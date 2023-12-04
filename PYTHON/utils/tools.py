import tiktoken
import json
from utils import globalsettings as gs


# https://github.com/openai/openai-cookbook/blob/main/examples/How_to_count_tokens_with_tiktoken.ipynb
def num_tokens_from_messages(messages, model="gpt-3.5-turbo-0613"):
    """Return the number of tokens used by a list of messages."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        print("Warning: model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")
    if model in {
        "gpt-3.5-turbo-1106",
        "gpt-3.5-turbo",
        "gpt-3.5-turbo-16k",
        "gpt-3.5-turbo-instruct",
        "gpt-3.5-turbo-0613",     # Legacy
        "gpt-3.5-turbo-16k-0613", # Legacy
        "gpt-4-32k",
        "gpt-4-1106-preview",   # GPT-4 Turbo
        "gpt-4-vision-preview", # GPT-4 Turbo with vision
        "gpt-4",
        "gpt-4-32k",
        "gpt-4-0613",
        "gpt-4-32k-0613"
        "gpt-4-0314",     # Legacy
        "gpt-4-32k-0314", # Legacy,
        }:
        tokens_per_message = 3
        tokens_per_name = 1
    elif model == "gpt-3.5-turbo-0301":
        tokens_per_message = 4  # every message follows <|start|>{role/name}\n{content}<|end|>\n
        tokens_per_name = -1  # if there's a name, the role is omitted
    elif "gpt-3.5-turbo" in model:
        print("Warning: gpt-3.5-turbo may update over time. Returning num tokens assuming gpt-3.5-turbo-0613.")
        return num_tokens_from_messages(messages, model="gpt-3.5-turbo-0613")
    elif "gpt-4" in model:
        print("Warning: gpt-4 may update over time. Returning num tokens assuming gpt-4-0613.")
        return num_tokens_from_messages(messages, model="gpt-4-0613")
    else:
        raise NotImplementedError(
            f"""num_tokens_from_messages() is not implemented for model {model}. See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens."""
        )
    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        if not isinstance(message, dict):
                continue
        for key, value in message.items():
            if key == 'function_call' or key == 'tool_calls':
                continue
            if value != None:
                num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
    return num_tokens



def bold(text):
    bold_start = "\033[1m"
    bold_end = "\033[0m"
    return bold_start + text + bold_end

def blue(text):
    blue_start = "\033[34m"
    blue_end = "\033[0m"
    return blue_start + text + blue_end

def red(text):
    red_start = "\033[31m"
    red_end = "\033[0m"
    return red_start + text + red_end


# Example dummy function hard coded to return the same weather
# In production, this could be your backend API or an external API
def get_current_weather(location, unit="fahrenheit"):
    """Get the current weather in a given location"""
    if "tokyo" in location.lower():
        return json.dumps({"location": "Tokyo", "temperature": "10", "unit": "celsius"})
    elif "san francisco" in location.lower():
        return json.dumps({"location": "San Francisco", "temperature": "72", "unit": "fahrenheit"})
    elif "paris" in location.lower():
        return json.dumps({"location": "Paris", "temperature": "22", "unit": "celsius"})
    else:
        return json.dumps({"location": location, "temperature": "unknown"})
    

tool_current_weather = {
            "type": "function",
            "function": {
                "name": "get_current_weather",
                "description": "Get the current weather in a given location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city and state, e.g. San Francisco, CA",
                        },
                        "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                    },
                    "required": ["location"],
                },
            },
        }

### TOOL: EXEC LOCAL CODE

tool_exec_local_code = {
    "type": "function",
    "function": {
        "name": "execute",
        "description": "Execute locally the python code provided as text",
        "parameters": {
            "type": "object",
            "properties": {
                "code": {
                    "type": "string",
                    "description": "Python code to be executed locally"
                },
            },
            "required": ["code"]
        },
    },
}


from utils.codeinterpreter import PythonInterpreter

the_interpreter = PythonInterpreter()

def execute(code):
    return the_interpreter.execute(code)

### TOOL: DOCUMENTATION RETRIEVER

tool_documentation_retriever = {
    "type": "function",
    "function": {
        "name": "retrieve_doc",
        "description": "Search in loaded documents to find useful functions to use in a prioritary manner",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The query to search for in the loaded documents"
                },
            },
            "required": ["query"]
        },
    },
}

from utils.docretriever import DocRetriever

persist_directory = gs.the_folders.VECTORSTORE
docs_directory    = gs.the_folders.MMM_DOCS
loader_kwargs = {'encoding': 'utf-8', 'csv_args': {'delimiter': ';'}}

the_doc_retriever = DocRetriever(
    persist_directory = persist_directory, 
    docs_directory    = docs_directory,
    loader_kwargs     = loader_kwargs
)

def retrieve_doc(query):
    res = the_doc_retriever.get_relevant_documents(query, search_type="mmr", k=4)
    out = "\n\n".join([x.page_content for x in res])
    return out

### TOOL: ADSTOCK FUNCTION
from mmm.tools import calculate_geom_ad_stock

the_interpreter.env["calculate_geom_ad_stock"] = calculate_geom_ad_stock

tool_calculate_geom_ad_stock = {
    "type": "function",
    "function": {
        "name": "calculate_geom_ad_stock",
        "description": "Calculate the geometric 'ad stock' of a data series by applying a decay factor.",
        "parameters": {
            "type": "object",
            "properties": {
                "series": {
                    "type": "List[float]",
                    "description": "List of values representing the investment or advertising impact in each period."
                },
                "decay_factor": {
                    "type": "float",
                    "description": "Decay factor that is applied to the accumulation of ad stock. If it is greater than 1, it is considered as a percentage and is internally divided by 100."
                },
                "initial_value": {
                    "type": "float",
                    "description": "Initial ad stock value. Defaults to 0."
                },
            },
            "required": ["series", "decay_factor"]
        },
    },
}


### AVAILABLE FUNCTIONS & TOOLS

available_functions = {
    'get_current_weather': get_current_weather,
    'execute': execute,
    'calculate_geom_adstock': calculate_geom_ad_stock,
    'retrieve_doc': retrieve_doc,
    }

tools_mmm = [
    tool_exec_local_code,
    tool_calculate_geom_ad_stock
]

