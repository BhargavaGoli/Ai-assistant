from openai import OpenAI
from dotenv import load_dotenv
import os


load_dotenv()

#create client with ollama local url, dummy key 
client = OpenAI(base_url='http://localhost:11434/v1', api_key='ollama')


#create reponse from chat.completions.create
stream = client.chat.completions.create(
    model="qwen3:4b",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Explain the plot of the movie Jurassic Park in 200 words"}
    ],
    stream=True
)

for chunk in stream :
    if chunk.choices[0].delta.content == None:
        continue
    print(chunk.choices[0].delta.content, end="", flush=True)