from utils.codeinterpreter import PythonInterpreter


the_interpreter = PythonInterpreter()

the_interpreter.execute("local_vars = __locals()__")
the_interpreter.get_var("local_vars")