import torch
import torch.nn as nn
import torch.nn.functional as F

class GPTConfig:
    def __init__(self, vocab_size, block_size, n_embd=64, n_head=4, n_layer=2):
        self.vocab_size = vocab_size
        self.block_size = block_size
        self.n_embd = n_embd
        self.n_head = n_head
        self.n_layer = n_layer
    
class SelfAttention(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.key = nn.Linear(config.n_embd, config.n_embd, bias=False)
        self.query = nn.Linear(config.n_embd, config.n_embd, bias=False)
        self.value = nn.Linear(config.n_embd, config.n_embd, bias=False)
        self.n_head = config.n_head
        self.head_dim = config.n_embd // config.n_head
    
    def forward(self, x):
        B, T, C = x.shape
        k = self.key(x).view(B, T, self.n_head, self.head_dim).transpose(1, 2)
        q = self.query(x).view(B, T, self.n_head, self.head_dim).transpose(1, 2)
        v = self.value(x).view(B, T, self.n_head, self.head_dim).transpose(1, 2)
        att = (q @ k.transpose(-2, -1)) / (self.head_dim ** 0.5)
        att = att.masked_fill(torch.triu(torch.ones(T, T), diagonal=1) == 1, float('-inf'))
        att = torch.softmax(att, dim=-1)
        out = att @ v
        out = out.transpose(1, 2).contiguous().view(B, T, C)  # reshape back
        return out

class TransformerBlock(nn.Module):
    
    def __init__(self, config):
        super().__init__()
        self.attn = SelfAttention(config)
        self.ln1 = nn.LayerNorm(config.n_embd)
        self.ff = nn.Sequential(
            nn.Linear(config.n_embd, 4 * config.n_embd),
            nn.ReLU(),
            nn.Linear(4 * config.n_embd, config.n_embd),
        )
        self.ln2 = nn.LayerNorm(config.n_embd)
        
    def forward(self, x):
        x = x + self.attn(self.ln1(x))  # attention + skip connection
        x = x + self.ff(self.ln2(x))    # feedforward + skip connection
        return x
        
class GPT(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.token_emb = nn.Embedding(config.vocab_size, config.n_embd)
        self.pos_emb = nn.Embedding(config.block_size, config.n_embd)
        self.blocks = nn.Sequential(*[TransformerBlock(config) for _ in range(config.n_layer)])
        self.ln_f = nn.LayerNorm(config.n_embd)
        self.head = nn.Linear(config.n_embd, config.vocab_size)
    
    def forward(self, idx):
        B, T = idx.shape
        tok = self.token_emb(idx)
        pos = self.pos_emb(torch.arange(T, device=idx.device))
        x = tok + pos
        x = self.blocks(x)
        x = self.ln_f(x)
        logits = self.head(x)
        return logits