import torch
from torch.utils.data import DataLoader
from torch import nn, optim
from dataset import TextDataset
from model import GPT, GPTConfig
from transformers import AutoTokenizer
import glob
import os

# === Configuration ===
block_size = 256
batch_size = 128
epochs = 200
checkpoint_dir = r"C:\Users\Utente\Desktop\TestLLM\data\epoch4_batch206882"
mid_epoch_saves = 1  # how many times per epoch to save mid-epoch
os.makedirs(checkpoint_dir, exist_ok=True)

# === Dataset Preparation ===
all_files = glob.glob(r"C:\Users\Utente\Desktop\TestLLM\data\paisa_sample_*_500.txt")
merged_path = r"C:\Users\Utente\Desktop\TestLLM\data\paisa_all.txt"

# Merge all text files into one training corpus
with open(merged_path, "w", encoding="utf-8") as out:
    for fname in all_files:
        with open(fname, encoding="utf-8") as f:
            out.write(f.read().strip() + "\n")

# === Tokenizer ===
tokenizer = AutoTokenizer.from_pretrained("gpt2")

# === Custom Text Dataset ===
ds = TextDataset(merged_path, block_size=block_size)
dataloader = DataLoader(ds, batch_size=batch_size, shuffle=True, num_workers=0)

# === Model ===
config = GPTConfig(
    vocab_size=tokenizer.vocab_size,  # ✅ use tokenizer vocab
    block_size=block_size,
    n_embd=64,
    n_head=4,
    n_layer=2
)
model = GPT(config)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# === Loss and Optimizer ===
loss_fn = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=1e-3)

# === Optional: Load previous checkpoint ===
checkpoint_path = r"C:\Users\Utente\Desktop\TestLLM\data\checkpoints\epoch3_batch0.pth"
if os.path.exists(checkpoint_path):
    checkpoint = torch.load(checkpoint_path, map_location="cpu")
    model.load_state_dict(checkpoint["model_state"])
    optimizer.load_state_dict(checkpoint["optimizer_state"])
    start_epoch = checkpoint.get("epoch", 0)
    start_batch = checkpoint.get("batch", 0)
    print(f"Resumed from checkpoint: epoch {start_epoch}, batch {start_batch}")
else:
    start_epoch = 0
    start_batch = 0
    print("No checkpoint found, starting from scratch.")

# === Training Loop with Checkpoints ===
for epoch in range(start_epoch, epochs):
    total_loss = 0
    print(f"\nEpoch {epoch+1}/{epochs}")
    
    for i, batch in enumerate(dataloader):
        if epoch == start_epoch and i < start_batch:
            print(i, 'skipped')
            continue

        x, y = batch
        x, y = x.to(device), y.to(device)

        logits = model(x)
        loss = loss_fn(logits.view(-1, config.vocab_size), y.view(-1))

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        total_loss += loss.item()

        # --- Mid-epoch checkpoint ---
        if i % max(1, len(dataloader) // mid_epoch_saves) == 0:
            ckpt_path = os.path.join(checkpoint_dir, f"epoch{epoch+1}_batch{i}.pth")
            torch.save({
                "epoch": epoch,
                "batch": i,
                "model_state": model.state_dict(),
                "optimizer_state": optimizer.state_dict(),
                "loss": loss.item(),
            }, ckpt_path)
            print(f"Checkpoint saved at batch {i}")

    avg_loss = total_loss / len(dataloader)
    print(f"Epoch {epoch+1}/{epochs}, Avg Loss: {avg_loss:.4f}")

    # --- End of epoch checkpoint ---
    ckpt_path = os.path.join(checkpoint_dir, f"epoch{epoch+1}_end.pth")
    torch.save({
        "epoch": epoch,
        "model_state": model.state_dict(),
        "optimizer_state": optimizer.state_dict(),
        "loss": avg_loss,
    }, ckpt_path)
    print(f"Checkpoint saved at epoch end: {ckpt_path}")

# === Final Model Save ===
final_path = r"C:\Users\Utente\Desktop\TestLLM\data\dataloader.pth"
torch.save(model.state_dict(), final_path)
print(f"\nTraining complete. Final model saved to {final_path}")
