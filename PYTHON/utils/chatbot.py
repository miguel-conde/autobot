import openai
from dotenv import load_dotenv
import os

from utils.contextmanager import ContextManager
from utils.tools import bold, blue, red

# Cargar variables de entorno del archivo .env
load_dotenv()

# Obtener la clave API de OpenAI del archivo .env
openai.api_key = os.getenv("OPENAI_API_KEY")

class ChatBot:
    
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
        
    def run_chatbot(self, **kwargs):
        
        while True:
            
            try:
            
                mensaje_usuario = input(bold(blue("Usuario: ")))
                if mensaje_usuario.lower() == "salir":
                    print("Chatbot: ¡Que te vaya bien!")
                    self.cm.print_history()
                    break
                self.cm.add_msg({'role': 'user', 'content': mensaje_usuario})
                
                respuesta = self.client.chat.completions.create(
                    model=self.model,  
                    messages=self.cm.historial_mensajes, 
                    max_tokens=self.max_tokens,
                    **kwargs
                )

                respuesta_chatbot = respuesta.choices[0].message.content.strip()
                print(bold(red(f"Chatbot: {respuesta_chatbot}")))
                self.cm.add_msg({'role': 'assistant', 'content': respuesta_chatbot})
                
            except KeyboardInterrupt:
                print("Chatbot: ¡Que te vaya bien!")
                break