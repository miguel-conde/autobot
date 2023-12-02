from utils.codeinterpreter import PythonInterpreter


the_interpreter = PythonInterpreter()

res = the_interpreter.execute("local_vars = locals()")
print(res)

res = the_interpreter.get_var("local_vars")
print(res)

res = the_interpreter.execute(
"""
import os

# Obtener el directorio actual
current_directory = os.getcwd()

# Obtener la lista de ficheros en el directorio actual
ficheros = os.listdir(current_directory)
ficheros
# Guardamos el resultado en la variable 'res'
res = f"Ficheros en {current_directory}: {ficheros}"
"""
)

print(res)