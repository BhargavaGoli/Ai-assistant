import requests
import json

from datetime import datetime

from Utilities.utilities import log
from rag import search_query


#run tool fucntion
def run_tool(call) :
    name = call.function.name
    arguments = call.function.arguments

    if name in available_tools :
        func = available_tools[name]
        try :
            args = json.loads(arguments) if arguments else {}
            log(f" 🔧 {name}: {arguments}")
            result = func(**args)
        except Exception as e :
            result = f"Error running {name} : {e}"
            print(result)
    else :
        result = "Unknown tool"
    
    text = str(result)
    log(f"  👉 returns : {text[:150]}{"..." if len(text) > 150 else ''}")

    return result

#tools method
def get_current_time() :
    """Return the current date and time"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_city_weather(city) :
    """Return the weather condition of city"""
    url = f"https://wttr.in/{city}?format=3"
    response = requests.get(url, timeout=10)
    return response.text.strip()

def get_current_city():
    """Return the user current city or home"""
    return "Bangalore"

#rag pipeline tool
def search_knowledge_base(query, top_k = 2) :
    result = search_query(query, top_k)
    log(f"📚 Searching Knowledge Base")

    for r in result :
        log(f"{r["name"]} - {r["id"]} - {r["similarity"]}")

    blocks = []
    for r in result :
        filename = r["name"]
        chunkid = r["id"]
        text = r["text"]
        blocks.append(f"{chunkid}\n{filename}\n{text}")

    return "\n\n".join(blocks)       

#TOOLS
TOOLS = [
    {
        "type" : "function",
        "function" :
        {
            "name" : "search_knowledge_base",
            "description" : "Search the Nimbus Tech company knowledge base. It covers: leave policy, "
                            "expense reimbursement, hiring process, technical interview guide, onboarding guide, "
                            "remote work policy, code of conduct and performance review process. "
                            "Use it for any question about company rules, benefits or HR processes. "
                            "Returns the most relevant passages with their source file.",
            "parameters" :
            {
                "type" : "object",
                "properties" : 
                {
                    "query" :
                    {
                        "type" : "string",
                        "description" : "The search query"
                    },
                },
                "required" : ["query"]
            }
        }
    },
    {
        "type" : "function",
        "function" :
        {
            "name" : "get_current_time",
            "description" : "This tool can be called when user mentioned current time or time",
            "parameters" :
            {
                "type" : "object",
                "properties" : {},
                "required" : []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_city",
            "description": "This tool can be called when user mentioned home or current city",
            "parameters" : {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type" : "function",
        "function" : 
        {
            "name" : "get_city_weather",
            "description" :  "Get the current weather for a city or country.",
            "parameters" : 
            {
                "type" : "object",
                "properties" : 
                {
                    "city" : 
                    {
                        "type" : "string",
                        "description" : "The city name"
                    },
                },
                "required" : ["city"]
            }
        }   
    },
]

available_tools = {
    "get_current_time": get_current_time,
    "get_city_weather": get_city_weather,
    "get_current_city": get_current_city,
    "search_knowledge_base" : search_knowledge_base,
}

