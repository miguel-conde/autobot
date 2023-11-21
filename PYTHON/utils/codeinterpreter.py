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
        try:
            # Ejecutar el código
            exec(code, self.env)
            # Almacenar el último resultado si es necesario
            if 'res' in self.env:
                self.last_result = self.env['res']
        except Exception as e:
            return str(e)

        return "Código ejecutado con éxito"
    
    def get_var(self, tgt_var):
        """_summary_

        Args:
            tgt_var (_type_): _description_

        Returns:
            _type_: _description_
        """        
        return self.env[tgt_var]