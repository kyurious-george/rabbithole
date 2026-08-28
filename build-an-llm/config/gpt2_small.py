from dataclasses import dataclass

@dataclass
class GPT2Config: 
    model_name: str = "gpt2-small (124M)"
    vocab_size: int = 50257
    context_length: int = 1024 
    emb_dim: int = 768
    n_heads: int = 12
    n_layers: int = 12
    drop_rate: float = 0.1
    qkv_bias: bool = True