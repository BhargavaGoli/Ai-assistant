from types import SimpleNamespace
from openai import OpenAI
from tools import *

client = OpenAI(base_url="http://localhost:11434/v1", api_key="dummy-key")

messages = [
    {
        "role": "system",
        "content": "You are a helpful assistant. don't use get_current_city tool"
    }
]

while True :
    prompt = input("you : ")

    if prompt.lower() == "exit" : break

    messages.append(
        {
            "role" : "user",
            "content" : prompt
        }
    )
    
    stream = client.chat.completions.create(
        model="qwen2.5:3b",
        messages=messages,
        tools=tools,
        stream=True,
    )
    
    print("LLM reponse")
    fullcontent = ""
    tool_frag = {}
    for chunk in stream :
        if not chunk : continue

        delta = chunk.choices[0].delta

        if delta.content : 
            print(delta.content, end="", flush=True)
            fullcontent += delta.content  

        if delta.tool_calls :
            for tc in delta.tool_calls:
                i = tc.index
                #not in dict
                if i not in tool_frag : tool_frag[i] = {"id": "", "name": "", "arguments": ""}
                #update id, name and arguments
                if tc.id : tool_frag[i]["id"] += tc.id
                if tc.function and tc.function.name : tool_frag[i]["name"] += tc.function.name 
                if tc.function and tc.function.arguments : tool_frag[i]["arguments"] += tc.function.arguments

    if tool_frag :

        for frag in tool_frag.values() :
            call = SimpleNamespace(
                id=frag["id"],
                function=SimpleNamespace(
                    name=frag["name"],
                    arguments=frag["arguments"]
                )
            )
            messages.append(
                {
                    "role": "assistant",
                    "content": fullcontent or "",
                    "tool_calls": [
                        {"id": call.id, "type": "function",
                        "function": {"name": call.function.name, "arguments": call.function.arguments}
                        }
                    ]
                }
            )
            result = run_tool(call)

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": call.id,
                    "content": str(result)
                }
            )
            print(f"tool called : {call.function.name}")

        follow_up = client.chat.completions.create(
            model="qwen2.5:3b",
            messages=messages,
            stream=True,
        )
        
        
        finaltext = ""
        for chunk in follow_up :
            if not chunk : continue
            d = chunk.choices[0].delta
            if d.content:
                print(d.content, end="", flush=True)
                finaltext += d.content
        print()
        messages.append({"role": "assistant", "content": finaltext})        
    else:
        print("\nno tool calls")
        messages.append(
            {
                "role": "assistant",
                "content": fullcontent
            }
        )

        

