from chapter5.data_processor import evaluate_model
from config.gpt2_small import GPT2Config
import tiktoken
from chapter5.data_processor import preprocess
from chapter5.data_processor import generate
import torch 
import numpy as np

from chapter4.gpt_architecture import GPTModel
from chapter5.gpt_download import download_and_load_gpt2
from chapter2.dataloader import create_dataloader_v1

def assign(l, r): 
    if l.shape != r.shape: 
        raise ValueError(f"Shape mismatch. Left: {l.shape}, Right {r.shape}")
    return torch.nn.Parameter(torch.tensor(r))

def load_weights_into_gpt(gpt, params):
    gpt.pos_emb.weight = assign(gpt.pos_emb.weight, params['wpe'])
    gpt.tok_emb.weight = assign(gpt.tok_emb.weight, params['wte'])

    for b in range(len(params["blocks"])): 
        q_w, k_w, v_w = np.split((params["blocks"][b]["attn"]["c_attn"])["w"], 3, axis=-1)
        gpt.trf_blocks[b].att.W_query.weight = assign(gpt.trf_blocks[b].att.W_query.weight, q_w.T)
        gpt.trf_blocks[b].att.W_key.weight = assign(gpt.trf_blocks[b].att.W_key.weight, k_w.T)
        gpt.trf_blocks[b].att.W_value.weight = assign(gpt.trf_blocks[b].att.W_value.weight, v_w.T)

        q_b, k_b, v_b = np.split((params["blocks"][b]["attn"]["c_attn"])["b"], 3, axis=-1)
        gpt.trf_blocks[b].att.W_query.bias = assign(gpt.trf_blocks[b].att.W_query.bias, q_b.T)
        gpt.trf_blocks[b].att.W_key.bias = assign(gpt.trf_blocks[b].att.W_key.bias, k_b.T)
        gpt.trf_blocks[b].att.W_value.bias = assign(gpt.trf_blocks[b].att.W_value.bias, v_b.T)

        gpt.trf_blocks[b].att.out_proj.weight = assign(gpt.trf_blocks[b].att.out_proj.weight, params["blocks"][b]["attn"]["c_proj"]["w"].T)
        gpt.trf_blocks[b].att.out_proj.bias = assign(gpt.trf_blocks[b].att.out_proj.bias, params["blocks"][b]["attn"]["c_proj"]["b"])

        gpt.trf_blocks[b].ff.layers[0].weight = assign(gpt.trf_blocks[b].ff.layers[0].weight, params["blocks"][b]["mlp"]["c_fc"]["w"].T)
        gpt.trf_blocks[b].ff.layers[0].bias = assign(gpt.trf_blocks[b].ff.layers[0].bias, params["blocks"][b]["mlp"]["c_fc"]["b"])
        
        gpt.trf_blocks[b].ff.layers[2].weight = assign(gpt.trf_blocks[b].ff.layers[2].weight, params["blocks"][b]["mlp"]["c_proj"]["w"].T)
        gpt.trf_blocks[b].ff.layers[2].bias = assign(gpt.trf_blocks[b].ff.layers[2].bias, params["blocks"][b]["mlp"]["c_proj"]["b"])

        gpt.trf_blocks[b].norm1.scale = assign(gpt.trf_blocks[b].norm1.scale, params["blocks"][b]["ln_1"]["g"])
        gpt.trf_blocks[b].norm1.shift = assign(gpt.trf_blocks[b].norm1.shift, params["blocks"][b]["ln_1"]["b"])

        gpt.trf_blocks[b].norm2.scale = assign(gpt.trf_blocks[b].norm2.scale, params["blocks"][b]["ln_2"]["g"])
        gpt.trf_blocks[b].norm2.shift = assign(gpt.trf_blocks[b].norm2.shift, params["blocks"][b]["ln_2"]["b"])

    gpt.final_norm.scale = assign(gpt.final_norm.scale, params["g"])
    gpt.final_norm.shift = assign(gpt.final_norm.shift, params["b"])
    gpt.out_head.weight = assign(gpt.out_head.weight, params["wte"])

def main(): 
    gpt = GPTModel(GPT2Config)
    gpt.eval()

    device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")

    settings, params = download_and_load_gpt2(model_size="124M", models_dir="gpt2")
    load_weights_into_gpt(gpt, params)
    gpt.to(device)

    tokenizer = tiktoken.get_encoding("gpt2")

    torch.manual_seed(123)
    token_ids = generate(
        model=gpt, 
        idx=preprocess("Every effort moves you", tokenizer).to(device), 
        max_new_tokens=25, 
        context_size=GPT2Config.context_length, 
        top_k=50, 
        temperature=1.5
    )

    file_path = 'data/the-verdict.txt'
    with open(file_path, 'r', encoding='utf-8') as f: 
        text_data = f.read()
        train_ratio = 0.90
        split_idx = int(train_ratio * len(text_data))
        train_data = text_data[:split_idx]
        val_data = text_data[split_idx:]
        train_loader = create_dataloader_v1(
            train_data, 
            batch_size=2, 
            max_length=GPT2Config.context_length, 
            stride=GPT2Config.context_length, 
            drop_last=False, 
            shuffle=False, 
            num_workers=0,
        )
        val_loader = create_dataloader_v1(
            val_data, 
            batch_size=2, 
            max_length=256, 
            stride=256, 
            drop_last=False, 
            shuffle=False, 
            num_workers=0,
        )
        train_loss, val_loss = evaluate_model(gpt, train_loader, val_loader, device, 5)

    print(train_loss, val_loss)

if __name__ == "__main__":
    main()