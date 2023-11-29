class PythonInterpreter:
    """_summary_
    """    
    def __init__(self):
        """_summary_
        """        
        self.env = {}
        self.last_result = None

    def execute(self, code):
        """_summary_

        Args:
            code (_type_): _description_

        Returns:
            _type_: _description_
        """        
        print(f"CODE:\n\n {code}")
        try:
            # Ejecutar el código
            exec(code, self.env)
            # Almacenar el último resultado si es necesario
            if 'res' in self.env:
                self.last_result = self.env['res']
                del self.env['res']
                print(f"res = {self.last_result}")
                return self.last_result
            else:
                self.last_result = None
                return "No has creado la variable 'res'"
        except Exception as e:
            return str(e)
       
    
    def get_var(self, tgt_var):
        """_summary_

        Args:
            tgt_var (_type_): _description_

        Returns:
            _type_: _description_
        """        
        return self.env[tgt_var]