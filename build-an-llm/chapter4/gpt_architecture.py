import torch
import torch.nn as nn

from config.gpt2_small import GPT2Config 
from chapter3.multihead_attention import MultiHeadedAttention

class GPTModel(nn.Module):
    def __init__(self, cfg):
        super().__init__()
        self.tok_emb = nn.Embedding(cfg.vocab_size, cfg.emb_dim)
        self.pos_emb = nn.Embedding(cfg.context_length, cfg.emb_dim)
        self.drop_emb = nn.Dropout(cfg.drop_rate)

        self.trf_blocks = nn.Sequential(
            *[TransformerBlock(cfg) for _ in range(cfg.n_layers)]
        )

        self.final_norm = LayerNorm(cfg.emb_dim)
        self.out_head = nn.Linear(
            cfg.emb_dim, cfg.vocab_size, bias=False
        )

    def forward(self, in_idx): 
        b, seq_len = in_idx.shape
        tok_embeds = self.tok_emb(in_idx)
        pos_embeds = self.pos_emb(
            torch.arange(seq_len, device=in_idx.device)
        )
        x = tok_embeds + pos_embeds
        x = self.drop_emb(x)
        x = self.trf_blocks(x)
        x = self.final_norm(x)
        logits = self.out_head(x)
        return logits

# ─────────────────────────────────────────────────────────────────────────────
# Transformer Components
# ─────────────────────────────────────────────────────────────────────────────

class TransformerBlock(nn.Module):
    def __init__(self, cfg): 
        super().__init__()
        self.att = MultiHeadedAttention(
            d_in=cfg.emb_dim, 
            d_out=cfg.emb_dim, 
            context_length=cfg.context_length,
            num_heads = cfg.n_heads, 
            dropout=cfg.drop_rate,
            qkv_bias=cfg.qkv_bias,
        )
        self.ff = FeedForward(cfg)
        self.norm1 = LayerNorm(cfg.emb_dim)
        self.norm2 = LayerNorm(cfg.emb_dim)
        self.drop_shortcut = nn.Dropout(cfg.drop_rate)
    
    def forward(self, x): 
        shortcut = x
        x = self.norm1(x)
        x = self.att(x)
        x = self.drop_shortcut(x)
        x = x + shortcut

        shortcut = x
        x = self.norm2(x)
        x = self.ff(x)
        x = self.drop_shortcut(x)
        x = x + shortcut
        return x


class GELU(nn.Module): 
    def __init__(self): 
        super().__init__()

    def forward(self, x): 
        return 0.5 * x * (1 + torch.tanh(
            torch.sqrt(torch.tensor(2.0 / torch.pi)) *
            (x + 0.044715 * torch.pow(x,3))
        ))


class FeedForward(nn.Module): 
    def __init__(self, cfg): 
        super().__init__()
        self.layers = nn.Sequential(
            nn.Linear(cfg.emb_dim, 4*cfg.emb_dim),
            GELU(), 
            nn.Linear(4 * cfg.emb_dim, cfg.emb_dim),
        )

    def forward(self, x):
        return self.layers(x)

# ─────────────────────────────────────────────────────────────────────────────
# Other Top Level Components
# ─────────────────────────────────────────────────────────────────────────────

class LayerNorm(nn.Module): 
    def __init__(self, emb_dim, eps=1e-5):
        super().__init__()
        self.eps = eps
        self.scale = nn.Parameter(torch.ones(emb_dim))
        self.shift = nn.Parameter(torch.zeros(emb_dim))

    def forward(self, x): 
        mean = x.mean(dim=-1, keepdim=True)
        var = x.var(dim=-1, keepdim=True, unbiased=False)
        norm_x = (x - mean) / torch.sqrt(var + self.eps)
        return self.scale * norm_x + self.shift


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────
def main(): 
    torch.manual_seed(123)
    model = GPTModel(GPT2Config())
    print("Total number of parameters in the Transformer Block modules", sum(p.numel() for p in model.trf_blocks.parameters()))
    n_mha_params = 0
    n_ff_params = 0
    for name, layer1 in model.trf_blocks.named_children():
        for name, layer2 in layer1.named_children(): 
            if isinstance(layer2, FeedForward): 
                n_ff_params += sum(p.numel() for p in layer2.parameters())
            if isinstance(layer2, MultiHeadedAttention): 
                n_mha_params += sum(p.numel() for p in layer2.parameters())
        
    print("Total number of parameters in the ff modules", n_ff_params)
    print("Total number of parameters in the mha modules", n_mha_params)

if __name__ == "__main__": 
    main()