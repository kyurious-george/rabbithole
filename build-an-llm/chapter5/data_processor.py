from torch.utils.data import DataLoader
import tiktoken
import torch

from chapter2.dataloader import create_dataloader_v1
from config.gpt2_small import GPT2Config
from chapter4.gpt_architecture import GPTModel

def preprocess(text: str, tokenizer: tiktoken.Encoding): 
    encoded = tokenizer.encode(text, allowed_special={'<|endoftext|>'})
    encoded_tensor = torch.tensor(encoded).unsqueeze(0)
    return encoded_tensor


def postprocess(token_ids: list[int], tokenizer: tiktoken.Encoding):
    flatten = token_ids.squeeze(0)
    return tokenizer.decode(flatten.tolist())


def calc_loss_batch(input_batch: torch.Tensor, target_batch: torch.Tensor, model, device): 
    input_batch = input_batch.to(device)
    target_batch = target_batch.to(device)
    logits = model(input_batch)
    loss = torch.nn.functional.cross_entropy(
        logits.flatten(0,1), target_batch.flatten()
    )
    return loss


def calc_loss_loader(data_loader: DataLoader, model, device, num_batches=None): 
    total_loss = 0
    if len(data_loader) == 0: 
        return float("nan")
    elif num_batches is None: 
        num_batches = len(data_loader)
    else: 
        num_batches = min(num_batches, len(data_loader))
    
    for i, (input_batch, target_batch) in enumerate(data_loader): 
        if i < num_batches: 
            loss = calc_loss_batch(
                input_batch, target_batch, model, device
            )
            total_loss += loss.item()
        else: 
            break 
    return total_loss / num_batches


def evaluate_model(model, train_loader, val_loader, device, eval_iter):
    model.eval()
    with torch.no_grad(): 
        train_loss = calc_loss_loader(train_loader, model, device, eval_iter)
        val_loss = calc_loss_loader(val_loader, model, device, eval_iter)
    model.train()
    return train_loss, val_loss


def generate_text_from_model(model, idx, max_new_tokens, context_size): 
    for _ in range(max_new_tokens): 
        idx_cond = idx[:, -context_size:]
        with torch.no_grad(): 
            logits = model(idx_cond)
        logits = logits[:, -1, :]
        probs = torch.softmax(logits, dim=-1)
        idx_next = torch.argmax(probs, dim=-1, keepdim=True)
        idx = torch.cat((idx, idx_next), dim=1)
    return idx


def generate_and_print_sample(model, tokenizer, device, start_context): 
    model.eval()
    context_size = model.pos_emb.weight.shape[0]
    encoded = preprocess(start_context, tokenizer).to(device)
    with torch.no_grad(): 
        token_ids = generate_text_from_model(model, encoded, 50, context_size)
    decoded_text = postprocess(token_ids, tokenizer)
    print(decoded_text.replace("\n", " "))
    model.train()


def train_model_simple(model, train_loader, val_loader, 
                       optimizer, device, num_epochs, eval_freq, 
                       eval_iter, start_context, tokenizer):
    train_losses, val_losses, track_tokens_seen = [], [], []
    tokens_seen, global_step = 0, -1

    for epoch in range(num_epochs): 
        model.train()
        for input_batch, target_batch in train_loader: 
            optimizer.zero_grad()
            loss = calc_loss_batch(input_batch, target_batch, model, device)
            loss.backward()
            optimizer.step()
            tokens_seen += input_batch.numel()
            global_step += 1

            if global_step % eval_freq == 0: 
                train_loss, val_loss = evaluate_model(model, train_loader, val_loader, device, eval_iter)
                train_losses.append(train_loss)
                val_losses.append(val_loss)
                track_tokens_seen.append(tokens_seen)
                print(f"Ep {epoch+1} (Step {global_step:06d}): "
                      f"Train loss {train_loss:.3f}"
                      f"Val loss {val_loss:.3f}"
                )
        generate_and_print_sample(model, tokenizer, device, start_context)
    return train_losses, val_losses, track_tokens_seen


def generate(
    model, 
    idx, 
    max_new_tokens, 
    context_size, 
    temperature=0.0, 
    top_k=None, 
    eos_id=None
):
    for _ in range(max_new_tokens): 
        idx_cond = idx[:, -context_size:]
        with torch.no_grad(): 
            logits = model(idx_cond)
        logits = logits[:, -1, :]
        if top_k is not None: 
            top_logits, _ = torch.topk(logits, top_k)
            min_val = top_logits[:, -1]
            logits = torch.where(
                logits < min_val, 
                torch.tensor(float('-inf')).to(logits.device),
                logits
            )
        if temperature > 0.0: 
            logits = logits / temperature
            probs = torch.softmax(logits, dim=-1)
            idx_next = torch.multinomial(probs, num_samples=1)
        else: 
            idx_next = torch.argmax(logits, dim=-1, keepdim=True)
        if idx_next == eos_id: 
            break 
        idx = torch.cat((idx, idx_next), dim=1)
    return idx

def main(): 
    torch.manual_seed(123)
    device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
    model = GPTModel(GPT2Config)
    # model.to(device)
    tokenizer = tiktoken.get_encoding("gpt2")
    optimizer = torch.optim.AdamW(model.parameters(), lr=0.0004, weight_decay=0.1)
    # num_epochs = 10

    # file_path = 'data/the-verdict.txt'
    # with open(file_path, 'r', encoding='utf-8') as f: 
    #     text_data = f.read()
    #     train_ratio = 0.90
    #     split_idx = int(train_ratio * len(text_data))
    #     train_data = text_data[:split_idx]
    #     val_data = text_data[split_idx:]
    #     train_loader = create_dataloader_v1(
    #         train_data, 
    #         batch_size=2, 
    #         max_length=GPT2Config.context_length, 
    #         stride=GPT2Config.context_length, 
    #         drop_last=False, 
    #         shuffle=False, 
    #         num_workers=0,
    #     )
    #     val_loader = create_dataloader_v1(
    #         val_data, 
    #         batch_size=2, 
    #         max_length=256, 
    #         stride=256, 
    #         drop_last=False, 
    #         shuffle=False, 
    #         num_workers=0,
    #     )
    #     train_losses, val_losses, tokens_seen = train_model_simple(
    #         model, train_loader, val_loader, optimizer, device, num_epochs, eval_freq=5, eval_iter=5, 
    #         start_context = "Every effort moves you", tokenizer=tokenizer
    #     )
    # torch.save({
    #     "model_state_dict": model.state_dict(), 
    #     "optimizer_state_dict": optimizer.state_dict(), 
    #     }, 
    #     "model_and_optimizer.pt"
    # )

    checkpoint = torch.load("model_and_optimizer.pt", map_location=device)
    model.load_state_dict(checkpoint["model_state_dict"])
    optimizer.load_state_dict(checkpoint["optimizer_state_dict"])
    model.train()

if __name__ == '__main__': 
    main()