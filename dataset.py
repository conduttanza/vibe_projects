import torch
from torch.utils.data import Dataset
from tokenizer import encode

class TextDataset(Dataset):
    def __init__(self, path, block_size):
        with open(path, 'r', encoding='utf-8', errors='replace') as f:
            raw = f.read()

        tokens = encode(raw)

        self.vocab_size = 256
        self.data = torch.tensor(tokens, dtype=torch.long)
        self.block_size = block_size

    def __len__(self):
        return max(1, len(self.data) - self.block_size)

    def __getitem__(self, idx):
        x = self.data[idx:idx + self.block_size]
        y = self.data[idx + 1:idx + 1 + self.block_size]
        return x, y
