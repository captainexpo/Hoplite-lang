import sys
import os
import Lexer
import Parser
import Eval
def use_file(file_name: str, e: Eval.Evaluator,args: list):
    if not os.path.isfile(file_name):
        print("File does not exist")
        return
    # get cwd from file name "../examples/benchmark.hpl" or such -> "../examples" given current file = "src/Hoplite1.py"

    full_path = os.path.dirname(file_name)
    #print("CWD", os.getcwd())
    #print("RELATIVE_TO_FILE", file_name)
    #print("FULL_PATH", full_path)
    absolute_path = os.path.abspath(full_path)
    e.file_path = absolute_path
    #print("ABSOLUTE_PATH", absolute_path)
   # print("E", e.file_path)
    # args format = [file_name, -f, file_name, -i (optional), include_file_name (optional)]
    # -f = file to use
    # -i = include file

    # if -i is in args, then include the file/directory
    if "-i" in args:
        include_name = args[args.index("-i") + 1]
        include_files = []
        if os.path.isdir(include_name):
            for file in os.listdir(include_name):
                if file.endswith(".hop"):
                    include_files.append(file)
        else:
            include_files.append(include_name)
        for file in include_files:
            if not os.path.isfile(file):
                print("Include file does not exist")
                return
            with open(file, "r") as f:
                include_file = f.read()
            tokens = Lexer.tokenize(include_file)
            ast = Parser.parse_program(tokens)
            
            e.execute(ast)
    with open(file_name, "r") as f:

        program = f.read()
    tokens = Lexer.tokenize(program)
    if "-tokens" in args:
        for i in tokens:
            print(i)
    ast = Parser.parse_program(tokens)
    if "-ast" in args: 
        for i in ast:
            print(i)
    e.execute(ast)
def use_as_repl(e: Eval.Evaluator):
    while True:
        program = input(">>> ")
        if program == "quit()":
            break
        try:
            tokens = Lexer.tokenize(program)
            ast = Parser.parse_program(tokens)
            e.execute(ast)
        except Exception as ex:
            print(ex)

def main():
    REPL_MODE = False
    ev = Eval.Evaluator()
    if "-r" in sys.argv:
        REPL_MODE = True
    if "-f" in sys.argv:
        use_file(sys.argv[2], ev, sys.argv)
        return
    else: 
        REPL_MODE = True
    if REPL_MODE: use_as_repl(ev)
    


if __name__ == "__main__":
    main()

