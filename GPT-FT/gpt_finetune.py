from openai import OpenAI
client = OpenAI()

fine_tunejobs = client.fine_tuning.jobs.create(
  training_file="file-tdT41CadgQ9veSIF9pkkki6I", 
  validation_file="file-5niQQTEeZA5Tp7eqeaAf3Xwe",
  suffix="arg_quality-0328",
  model="gpt-3.5-turbo-0125",
  hyperparameters={
    "n_epochs":3
  }
)

print(fine_tunejobs)

