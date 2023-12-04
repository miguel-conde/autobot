import openai
from dotenv import load_dotenv
import os
import time
from utils.tools import bold, blue, red
from utils import globalsettings as gs

# Cargar variables de entorno del archivo .env
load_dotenv()

# Obtener la clave API de OpenAI del archivo .env
openai.api_key = os.getenv("OPENAI_API_KEY")

client = openai.OpenAI()

# Upload a file with an "assistants" purpose
file = client.files.create(
  file    = open(gs.the_files.MMM_DOCS, "rb"),
  purpose = 'assistants'
)

# Step 1: Create an Assistant
assistant = client.beta.assistants.create(
    name         = "MMM Assistant",
    description  = "Un copiloto para proyectos MMM, capaz de generar código y ejecutarlo localmente",
    instructions = gs.prj_prompts.DIRECTIVA_PYTHON_PROGRAMMER3,
    tools        = [{"type": "retrieval"}],
    model        = "gpt-3.5-turbo-1106",
    file_ids     = [file.id]
)

# Step 2: Create a Thread
thread = client.beta.threads.create()


while True:
  
  try:
    mensaje_usuario = input(bold(blue("Usuario: ")))
    if mensaje_usuario.lower() == "salir":
        print(bold(red("Chatbot: ¡Que te vaya bien!")))
        break
      
    # Step 3: Add a Message to a Thread
    message = client.beta.threads.messages.create(
        thread_id = thread.id,
        role      = "user",
        content   = mensaje_usuario
    )

    # thread_messages = client.beta.threads.messages.list(thread.id)
    # print(thread_messages.data)

    # Step 4: Run the Assistant
    run = client.beta.threads.runs.create(
      thread_id    = thread.id,
      assistant_id = assistant.id,
    )

    while True:
      # Step 5: Check the Run status
      run = client.beta.threads.runs.retrieve(
        thread_id = thread.id,
        run_id    = run.id
      )
      print(run.status)

      if run.status == 'completed':
        # Step 6: Display the Assistant's Response
        messages = client.beta.threads.messages.list(
          thread_id = thread.id
        )

        [print(x.content[0].text.value+"\n######") for x in messages.data]

      if run.status in ['expired', 'completed', 'failed', 'cancelled']:
        break
      
      time.sleep(5)
  except KeyboardInterrupt:
      print(bold(red("Chatbot: Hasta la vista!")))
      break

