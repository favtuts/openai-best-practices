import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
print("API_KEY: " + OPENAI_API_KEY)

client = OpenAI(
    api_key=OPENAI_API_KEY,
)

completion = client.chat.completions.create(
  # model="gpt-4o-mini",
  model="gpt-3.5-turbo",  
  messages=[
    {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
    {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
  ]
)

print(completion.choices[0].message)