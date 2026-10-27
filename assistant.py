from openai import OpenAI
from dotenv import load_dotenv
import os
import json
from tools import tools, get_current_time, available_tools
load_dotenv()

#creating client connection
client = OpenAI(
    base_url = os.getenv("URL"),
    api_key = os.getenv("API_KEY")
)

messages = [
    {
        "role": "system",
        "content": "You are a helpful assistant and respond within 20 words"
    }
]

while True :
    prompt = input("you : ")

    if prompt.lower() in ("exit", "bye") :
        print("llm response ended")
        break
    
    messages.append(
        {
            "role" : "user",
            "content" : prompt
        }
    )

    response = client.chat.completions.create(
        model = os.getenv("MODEL"),
        messages = messages, 
        tools = tools
    )

    reply = response.choices[0].message

    if reply.tool_calls :

        for call in reply.tool_calls :
            name = call.function.name
            arguments = call.function.arguments

            if name in available_tools :
                func = available_tools[name]
                try :
                    args = json.loads(arguments) if arguments else {}
                    result = func(**args)
                except Exception as e :
                    result = f"Error running {name} : {e}"
                    print(result)
            else :
                result = "Unknown tool"
    
            messages.append(
                {
                    "role" : "tool",
                    "tool_call_id" : call.id,
                    "content" : result
                }
            )

        follow_up = client.chat.completions.create(
            model = os.getenv("MODEL"),
            messages = messages,
            tools = tools
        )

        reply = follow_up.choices[0].message

        messages.append(
            {
                "role" : reply.role,
                "content" : reply.content
            }
        )          

        print("LLM response : " + reply.content)
    else :

        messages.append(
            {
                "role" : reply.role,
                "content" : reply.content
            }
        )

        print("llm response : " + reply.content)

rdt = response.model_dump()

print(json.dumps(rdt, indent = 4))