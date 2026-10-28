from datetime import datetime

#get_curret_time tool for ai agent
def get_current_time() :
    """Return the current date and time"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

#TOOLS
tools = [
    {
        "type" : "function",
        "function" :
        {
            "name" : "get_current_time",
            "description" : "Get the current date and time",
            "parameters" :
            {
                "type" : "object",
                "properties" : {},
                "required" : []
            }
        }
    }
]

available_tools = {
    "get_current_time" : get_current_time
}
