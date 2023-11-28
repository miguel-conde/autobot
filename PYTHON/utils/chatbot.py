import openai
from dotenv import load_dotenv, find_dotenv
import os
import json
from tenacity import retry, wait_random_exponential, stop_after_attempt

from utils.contextmanager import ContextManager
from utils.tools import bold, blue, red
from utils.tools import tool_current_weather, get_current_weather

# Cargar variables de entorno del archivo .env
load_dotenv()

# Obtener la clave API de OpenAI del archivo .env
openai.api_key = os.getenv("OPENAI_API_KEY")

class ChatBot:
    
    tools = [
        tool_current_weather,
    ]
    
    available_functions = {
        'get_current_weather': get_current_weather,
    }
    
    def __init__(
        self, 
        model                 = "gpt-3.5-turbo-1106", 
        directiva_del_sistema = "You're a helpful assistant", 
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
        self.model      = model
        self.max_tokens = max_tokens
        
    @retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3))
    def chat_completion_request(self, tool_choice="none", **kwargs):
        """_summary_

        Args:
            tool_choice (str, optional): _description_. Defaults to "none".

        Returns:
            _type_: _description_
        """        
        respuesta = self.client.chat.completions.create(
                    model       = self.model,  
                    messages    = self.cm.historial_mensajes, 
                    max_tokens  = self.max_tokens,
                    tools       = ChatBot.tools,
                    tool_choice = tool_choice,
                    **kwargs
                )
        return respuesta
        
        
    def run_chatbot(self, **kwargs):
        
        while True:
            
            try:
            
                mensaje_usuario = input(bold(blue("Usuario: ")))
                if mensaje_usuario.lower() == "salir":
                    print(bold(red("Chatbot: ¡Que te vaya bien!")))
                    # self.cm.print_history()
                    break
                self.cm.add_msg({'role': 'user', 'content': mensaje_usuario})
                
                # respuesta = self.client.chat.completions.create(
                #     model       = self.model,  
                #     messages    = self.cm.historial_mensajes, 
                #     max_tokens  = self.max_tokens,
                #     tools       = ChatBot.tools,
                #     tool_choice = "auto", # TODO Check this
                #     **kwargs
                # )
                respuesta = self.chat_completion_request(tool_choice = "auto", **kwargs)

                mensaje_respuesta = respuesta.choices[0].message
                
                tool_calls = mensaje_respuesta.tool_calls
                if tool_calls: # El modelo quiere llamar a alguna función
                    
                    # self.cm.add_msg(mensaje_respuesta.dict())
                    self.cm.add_msg(mensaje_respuesta)
                    for tool_call in tool_calls:
                        # Ejecutamos la función localmente
                        function_name = tool_call.function.name
                        function_to_call = ChatBot.available_functions[function_name]
                        function_args = json.loads(tool_call.function.arguments)
                        function_response = function_to_call(
                            **function_args,
                        )
                        # Añadimos el resultado al contecto
                        self.cm.add_msg(
                            {
                                "tool_call_id": tool_call.id,
                                "role": "tool",
                                "name": function_name,
                                "content": function_response,
                            }
                        )
                        
                    # Pasamos al LLM el contecto actualizado con el resultado de la función 
                    # segunda_respuesta = self.client.chat.completions.create(
                    #     model       = self.model,  
                    #     messages    = self.cm.historial_mensajes, 
                    #     max_tokens  = self.max_tokens,
                    #     **kwargs
                    # )
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
                print("Chatbot: ¡Que te vaya bien!")
                break