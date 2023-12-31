
import pandas as pd

from utils.tools import num_tokens_from_messages

class ContextManager:
    """_summary_
    """    
    def __init__(self, model, directiva_del_sistema = "You're a helpful assitant", max_tokens_context = 8000):
        """_summary_

        Args:
            model (_type_): _description_
            directiva_del_sistema (str, optional): _description_. Defaults to "You're a helpful assitant".
            max_tokens_context (int, optional): _description_. Defaults to 8000.
        """        
        self.directiva_del_sistema = directiva_del_sistema
        self.historial_mensajes = [{'role': 'system', 'content': directiva_del_sistema}]
        self.model = model
        self.max_tokens_context = max_tokens_context
        
    def add_msg(self, nuevo_mensaje):
        """_summary_

        Args:
            nuevo_mensaje (_type_): _description_

        Raises:
            ValueError: _description_
        """        
        self.historial_mensajes.append(nuevo_mensaje)
        
        if num_tokens_from_messages(self.historial_mensajes, self.model) > self.max_tokens_context:
            raise ValueError("The prompt is too long. Please reduce the size of the file.")
        
    def get_history(self):
        """_summary_

        Returns:
            _type_: _description_
        """        
        return pd.DataFrame(self.historial_mensajes)
        
    def print_history(self):
        """_summary_
        """        
        for item in self.historial_mensajes:
            print(f"{item['role']}: {item['content']}")
            
            
            

        