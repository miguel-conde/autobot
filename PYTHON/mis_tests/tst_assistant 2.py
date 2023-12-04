import openai
from dotenv import load_dotenv
import os
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
    name         = "MMM Assitant",
    description  = "Un copiloto para proyectos MMM, capaz de generar código y ejecutarlo localmente",
    instructions = gs.prj_prompts.DIRECTIVA_PYTHON_PROGRAMMER2,
    tools        = [{"type": "retrieval"}],
    model        = "gpt-4-1106-preview",
    file_ids     = [file.id]
)

# Step 2: Create a Thread
thread = client.beta.threads.create()

# Step 3: Add a Message to a Thread
message = client.beta.threads.messages.create(
    thread_id = thread.id,
    role      = "user",
    content   = "Tenemos un modelo lineal ajustado, fit_lm. Calcula su coeficiente de determinación."
)

thread_messages = client.beta.threads.messages.list(thread.id)
print(thread_messages.data)

# Step 4: Run the Assistant
run = client.beta.threads.runs.create(
  thread_id    = thread.id,
  assistant_id = assistant.id,
  # instructions=" Recuerda que en el codigo que generes para ejecutar localmente debes asignar a la variable 'res' el texto que te permita saber el resultado que tu necesitas."
)

# Step 5: Check the Run status
run = client.beta.threads.runs.retrieve(
  thread_id = thread.id,
  run_id    = run.id
)

print(run.status)

# Step 6: Display the Assistant's Response
messages = client.beta.threads.messages.list(
  thread_id = thread.id
)

messages.data[0].__dict__

print(messages.data[0].content[0].text.value)

[print(x.content[0].text.value+"\n######") for x in messages.data]