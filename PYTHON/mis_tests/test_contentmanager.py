from utils.contextmanager import ContextManager


cm = ContextManager(model="gpt-3.5-turbo-1106")

cm.print_history()

cm.add_msg({'role': 'user', 'content': "Soy el usuario"})

cm.print_history()

cm.add_msg({'role': 'assistant', 'content': "Soy el asistente"})

cm.print_history()

cm.get_history()