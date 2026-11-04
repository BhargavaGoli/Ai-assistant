#standard lib
import os
#third-party lib
from openai import OpenAI
from dotenv import load_dotenv
from types import SimpleNamespace
#local_modules
from tools import TOOLS, run_tool
from Utilities.utilities import log

load_dotenv()

#creating client connection
client = OpenAI(
    base_url = os.getenv("URL"),
    api_key = os.getenv("API_KEY")
)

messages = [
    {
        "role": "system",
        "content": (
            "You are a helpful assistant with access to tools.\n\n"
        )
    }
]

def stream_data(history) :
    stream = client.chat.completions.create(
            model = os.getenv("MODEL"),
            messages = history, 
            tools = TOOLS,
            stream = True
    )

    label_printed = False
        
    fullcontent = ""
    tool_frag = {}
    try :
        for chunk in stream :
            if not chunk.choices : continue 

            delta = chunk.choices[0].delta

            if delta.content : 
                if not label_printed : 
                    print("👾 llm response : ", end = "", flush = True)
                    label_printed = True
                print(delta.content, end = "", flush = True)
                fullcontent += delta.content

            if delta.tool_calls :
                for tc in delta.tool_calls :
                    idx = tc.index
                    if idx not in tool_frag : tool_frag[tc.index] = {"id" : "", "type": "function", "function" : {"name" : "", "arguments" : ""}}

                    if tc.id : tool_frag[idx]["id"] = tc.id
                    if tc.function and tc.function.name : tool_frag[idx]["function"]["name"] += tc.function.name
                    if tc.function and tc.function.arguments : tool_frag[idx]["function"]["arguments"] += tc.function.arguments
    except KeyboardInterrupt :
        print(f"\n----STOPPED BY YOU----")
        tool_frag = {}

    if label_printed : print()

    return fullcontent, list(tool_frag.values())

def convert_to_apiformat(calls) :
    calls_list = []
    for frag in calls :
        call = SimpleNamespace(
            id = frag["id"],
            function = SimpleNamespace(
                name = frag["function"]["name"],
                arguments = frag["function"]["arguments"]
            )
        )
        calls_list.append(call)

    return calls_list


log(f"{os.getenv("MODEL")}")
while True :
    prompt = input("❤️  you : ")

    if prompt.lower() in ("exit", "bye") :
        print("llm response ended")
        break
    
    messages.append(
        {
            "role" : "user",
            "content" : prompt
        }
    )
    
    MAX_STEPS = 5 
    for step in range(MAX_STEPS) : # Agent <-> LLM

        content, calls = stream_data(messages) 
        formattedcalls = convert_to_apiformat(calls) 

        if calls == [] : break     

        log(f" step {step + 1} : model requested {len(calls)} tool calls")

        messages.append({
            "role": "assistant",
            "content": content,
            "tool_calls": calls
        })

        for call in formattedcalls :
            result = run_tool(call)
            messages.append({
                "role": "tool",
                "tool_call_id" : call.id,
                "content": str(result) 
            })

    else :
        fallback = "Sorry, I could not finish this within the step limit."
        messages.append({
            "role": "assistant", "content": fallback
        })
        print("👾 LLM response : "+ fallback)
        continue
    
    messages.append(
        {
            "role" : "assistant",
            "content" : content
        }
    )          



# rdt = response.model_dump()

# print(json.dumps(rdt, indent = 4))