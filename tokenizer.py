from transformers import AutoTokenizer

# Load the same tokenizer used for training
_tokenizer = AutoTokenizer.from_pretrained("gpt2")

def encode(text):
    return _tokenizer.encode(text, add_special_tokens=False)

def decode(tokens):
    return _tokenizer.decode(tokens)
