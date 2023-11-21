class PythonInterpreter:
    def __init__(self):
        self.env = {}
        self.last_result = None

    def execute(self, code):
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
        
        return self.env[tgt_var]