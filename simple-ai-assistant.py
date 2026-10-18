from openai import OpenAI

client = OpenAI(
    base_url="http://127.0.0.1:11434/v1",
    api_key="YOUR_API_KEY"
)

response =client.chat.completions.create(
    model="qwen3:1.7b",
    messages=[
        {
            "role": "user",
            "content": "hello, who are you?"
        }
    ]
)

# Print the assistant's message content
print(response.choices[0].message.content)