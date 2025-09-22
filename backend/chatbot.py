from transformers import BlenderbotTokenizer, BlenderbotForConditionalGeneration
import torch

MODEL_NAME = "facebook/blenderbot-3B"

tokenizer = BlenderbotTokenizer.from_pretrained(MODEL_NAME)
model = BlenderbotForConditionalGeneration.from_pretrained(MODEL_NAME)
model.eval()  # inference mode

# warmup (reduces first-request latency)
_ = tokenizer("hello", return_tensors="pt")

@torch.no_grad()
def generate_reply(user_input: str) -> str:
    inputs = tokenizer(user_input, return_tensors="pt")
    reply_ids = model.generate(
        **inputs,
        max_new_tokens=120,
        do_sample=True,
        temperature=0.7,
        top_p=0.9,
        repetition_penalty=1.1
    )
    return tokenizer.decode(reply_ids[0], skip_special_tokens=True)
