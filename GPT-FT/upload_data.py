from openai import OpenAI
client = OpenAI()

client.files.create(
  file=open("gpt_dev.jsonl", "rb"),
  purpose="fine-tune"
)