from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

#creating a ollama connection
client = OpenAI(
    base_url = os.getenv("URL"), 
    api_key = os.getenv("API_KEY")
)

while True :
    user_input = input("you: ")
    
    if user_input.lower() in ("quit", "exit", "bye") :
        print("LLM response stopped")
        break

    response = client.chat.completions.create(
        model = os.getenv("MODEL"), 
        messages = [
            {
                "role": "user",
                "content": user_input + "/no_think" + "talk in english"
            }
        ]
    )

    print("LLM response: " ) 
    print(response.choices[0].message.content)