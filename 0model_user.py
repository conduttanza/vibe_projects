import torch
from model import GPT, GPTConfig
from tokenizer import encode, decode

# === Model Configuration ===
config = GPTConfig(
    vocab_size=50257,   # ✅ matches GPT-2 / your tokenizer’s vocab
    block_size=256,
    n_embd=64,
    n_head=4,
    n_layer=2
)

# === Initialize Model ===
model = GPT(config)

# === Load trained weights ===
# If you want to use a mid-epoch checkpoint, uncomment this:
# checkpoint = torch.load(r"C:\Users\Utente\Desktop\TestLLM\data\checkpoints\epoch4_batch206882.pth", map_location="cpu")
# model.load_state_dict(checkpoint['model_state'])

# Otherwise, load the final trained model:
model.load_state_dict(torch.load(
    r"C:\Users\Utente\Desktop\TestLLM\data\dataloader.pth",
    map_location="cpu"
))

model.eval()
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# === Text Generation ===
start_text = input("Input di testo:\n")
input_ids = torch.tensor([encode(start_text)], dtype=torch.long).to(device)

max_new_tokens = 50
temperature = 0.1  # higher = more creative, lower = more deterministic
generated = input_ids.clone()

for _ in range(max_new_tokens):
    # Take the last block_size tokens as input
    x_in = generated[:, -config.block_size:]

    with torch.no_grad():  # disables gradient tracking
        logits = model(x_in)

    # Get logits for the last predicted token
    last_token_logits = logits[:, -1, :] / temperature

    # Convert logits to probabilities
    probs = torch.softmax(last_token_logits, dim=-1)

    # Sample the next token from the probability distribution
    next_token = torch.multinomial(probs, num_samples=1)

    # Append the predicted token
    generated = torch.cat((generated, next_token), dim=1)

# === Decode generated output ===
output_text = decode(generated[0].tolist())
print("\n=== Generated text ===\n")
print(output_text)

# === Save output ===
output_path = r"C:\Users\Utente\Desktop\TestLLM\data\generated_output.txt"
with open(output_path, "w", encoding="utf-8") as f:
    f.write(output_text)

#print(f"\nGenerated sequence saved to {output_path}")
