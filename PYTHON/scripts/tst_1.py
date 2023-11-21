import openai
from dotenv import load_dotenv
import os

from utils import globalsettings as gs
from utils.contextmanager import ContextManager

# Cargar variables de entorno del archivo .env
load_dotenv()

# Obtener la clave API de OpenAI del archivo .env
openai.api_key = os.getenv("OPENAI_API_KEY")

client = openai.OpenAI()

# historial_mensajes = [{'role': 'system', 'content': 'You are a helpful assistant.'}]
cm = ContextManager()
while True:
    
    mensaje_usuario = input("Usuario: ")
    if mensaje_usuario.lower() == "salir":
        print("Chatbot: ¡Que te vaya bien!")
        cm.print_history()
        break
    # historial_mensajes.append({'role': 'user', 'content': mensaje_usuario})
    cm.add_msg({'role': 'user', 'content': mensaje_usuario})
    
    respuesta = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",  # O el modelo que prefieras usar
        messages=cm.historial_mensajes,
        max_tokens=150
    )

    respuesta_chatbot = respuesta.choices[0].message.content.strip()
    print("Chatbot:", respuesta_chatbot)
    # historial_mensajes.append({'role': 'assistant', 'content': respuesta_chatbot})
    cm.add_msg({'role': 'assistant', 'content': respuesta_chatbot})
