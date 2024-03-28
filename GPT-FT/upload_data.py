from openai import OpenAI
client = OpenAI()

training_file = client.files.create(
  file=open("gpt_test.jsonl", "rb"),
  purpose="fine-tune"
)

print(training_file.id)     

