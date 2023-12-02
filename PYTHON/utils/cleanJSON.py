# https://scriv.ai/guides/openai-functions-json/

import openai
import json


clean_json_fn = {
    "name": "clean_json",
    "description": "Cleans JSON.",
    "parameters": {
        "type": "object",
        "properties": {
            "clean_json": {
                "type": "string",
                "description": "The cleaned JSON.",
            },
        },
        "required": ["clean_json"],
    },
}




class JSONCleaner:
    
    def __init__(self):
        self.client = openai.OpenAI()
        
    def clean_json(self, bad_json):
        
        messages = [
            {
                "role": "system",
                "content": "You are a helpful assistant.",
                },
            {
                "role": "user",
                "content": f"The bad JSON: {bad_json}",
                },
            ]
        
        openai_response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            functions=[clean_json_fn],
            function_call={"name": clean_json_fn["name"]},
            )
        
        arguments_raw = openai_response.choices[0].message.function_call.arguments
        arguments = json.loads(arguments_raw)
        cleaned_json_raw = arguments["clean_json"]
        
        return(cleaned_json_raw)


