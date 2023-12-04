import openai
from dotenv import load_dotenv
import os
import json
from tenacity import retry, wait_random_exponential, stop_after_attempt

from utils.contextmanager import ContextManager
from utils.tools import bold, blue, red
# from utils.tools import tool_current_weather, get_current_weather, tool_exec_local_code
# from utils.codeinterpreter import PythonInterpreter
from utils.cleanJSON import JSONCleaner
from utils.docretriever import DocRetriever


# Cargar variables de entorno del archivo .env
load_dotenv()

# Obtener la clave API de OpenAI del archivo .env
openai.api_key = os.getenv("OPENAI_API_KEY")

# the_interpreter = PythonInterpreter()
# 
# def execute(code):
#     return the_interpreter.execute(code)

class ChatBot:
    
    def __init__(
        self, 
        model                 = "gpt-3.5-turbo-1106", 
        directiva_del_sistema = "You're a helpful assistant", 
        tools                 = [],
        available_functions   = {},
        max_tokens_contexto   = 8000, 
        max_tokens            = 150
        ):
        """_summary_

        Args:
            model (str, optional): _description_. Defaults to "gpt-3.5-turbo-1106".
            directiva_del_sistema (str, optional): _description_. Defaults to "You're a helpful assistant".
            max_tokens_contexto (int, optional): _description_. Defaults to 8000.
            max_tokens (int, optional): _description_. Defaults to 150.
        """        
        self.client     = openai.OpenAI()
        self.cm         = ContextManager(
            model                 = model, 
            directiva_del_sistema = directiva_del_sistema, 
            max_tokens_context    = max_tokens_contexto
            )
        self.model               = model
        self.max_tokens          = max_tokens
        self.tools               = tools
        self.available_functions = available_functions
        self.the_JSON_cleaner    = JSONCleaner()
        
    @retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3))
    def chat_completion_request(self, tool_choice="none", **kwargs):
        """_summary_

        Args:
            tool_choice (str, optional): _description_. Defaults to "none".

        Returns:
            _type_: _description_
        """        
        try:
            respuesta = self.client.chat.completions.create(
                        model       = self.model,  
                        messages    = self.cm.historial_mensajes, 
                        max_tokens  = self.max_tokens,
                        tools       = self.tools,
                        tool_choice = tool_choice,
                        temperature = 0,
                        **kwargs
                    )
            return respuesta
        # https://help.openai.com/en/articles/6897213-openai-library-error-types-guidance
        except openai.error.Timeout as e:
            # Handle timeout error, e.g. retry or log
            print(f"OpenAI API request timed out: {e}")
            pass
        except openai.error.APIError as e:
          # Handle API error, e.g. retry or log
          print(f"OpenAI API returned an API Error: {e}")
          pass
        except openai.error.APIConnectionError as e:
          # Handle connection error, e.g. check network or log
          print(f"OpenAI API request failed to connect: {e}")
          pass
        except openai.error.InvalidRequestError as e:
          # Handle invalid request error, e.g. validate parameters or log
          print(f"OpenAI API request was invalid: {e}")
          pass
        except openai.error.AuthenticationError as e:
          # Handle authentication error, e.g. check credentials or log
          print(f"OpenAI API request was not authorized: {e}")
          pass
        except openai.error.PermissionError as e:
          # Handle permission error, e.g. check scope or log
          print(f"OpenAI API request was not permitted: {e}")
          pass
        except openai.error.RateLimitError as e:
          # Handle rate limit error, e.g. wait or log
          print(f"OpenAI API request exceeded rate limit: {e}")
          pass
      
    def fix_json_function_args(self, bad_json):
        try:
            function_args = json.loads(bad_json)
        except json.JSONDecodeError:
            cleaned_json_raw = self.the_JSON_cleaner.clean_json(bad_json)
            function_args = json.loads(cleaned_json_raw)
            
        return function_args
        
    def run_chatbot(self, **kwargs):
        
        while True:
            
            try:
            
                mensaje_usuario = input(bold(blue("Usuario: ")))
                if mensaje_usuario.lower() == "salir":
                    print(bold(red("Chatbot: ¡Que te vaya bien!")))
                    # self.cm.print_history()
                    break
                the_user_content = mensaje_usuario +\
                    " Recuerda que en el codigo que generes para ejecutar localmente debes asignar a la variable 'res' el texto que te permita saber el resultado que tu necesitas." + \
                    " Por favor, genera siempre código limpio, sin ponerlo entre ```\{python\} y ```"
                self.cm.add_msg({'role': 'user', 'content': the_user_content})
                respuesta = self.chat_completion_request(tool_choice = "auto", **kwargs)

                mensaje_respuesta = respuesta.choices[0].message
                
                tool_calls = mensaje_respuesta.tool_calls
                if tool_calls: # El modelo quiere llamar a alguna función
                    
                    # self.cm.add_msg(mensaje_respuesta.dict())
                    self.cm.add_msg(mensaje_respuesta)
                    for tool_call in tool_calls:
                        # Ejecutamos la función localmente
                        function_name = tool_call.function.name
                        if function_name in self.available_functions:
                            function_to_call = self.available_functions[function_name]
                            try:
                                function_args = json.loads(tool_call.function.arguments)
                            except json.JSONDecodeError:
                                cleaned_json_raw = self.the_JSON_cleaner.clean_json(tool_call.function.arguments)
                                function_args = json.loads(cleaned_json_raw)
                            print(function_args)
                            function_response = function_to_call(
                                **function_args,
                            )
                        else:
                            function_response = "Esa función no existe"
                        
                        # Añadimos el resultado al contexto
                        self.cm.add_msg(
                            {
                                "tool_call_id": tool_call.id,
                                "role": "tool",
                                "name": function_name,
                                "content": function_response,
                            }
                        )
                        
                    # Pasamos al LLM el contexto actualizado con el resultado de la función 
                    segunda_respuesta = self.chat_completion_request(tool_choice = "none", **kwargs)
                        
                    mensaje_segunda_respuesta = segunda_respuesta.choices[0].message
                    segunda_respuesta_chatbot = mensaje_segunda_respuesta.content.strip()
                    print(bold(red(f"Chatbot: {segunda_respuesta_chatbot}")))
                    self.cm.add_msg({'role': 'assistant', 'content': segunda_respuesta_chatbot})
                        
                else:
                    respuesta_chatbot = mensaje_respuesta.content.strip()
                    print(bold(red(f"Chatbot: {respuesta_chatbot}")))
                    self.cm.add_msg({'role': 'assistant', 'content': respuesta_chatbot})
                
            except KeyboardInterrupt:
                # print(bold(red("Chatbot: Interrumpido por usuario")))
                # pass
                print(bold(red("Chatbot: Hasta la vista!")))
                break