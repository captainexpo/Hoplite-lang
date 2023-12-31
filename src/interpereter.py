import sys
import os
import lexer_class
import parser_class
import evaluator
def use_file(file_name: str, e: evaluator.Evaluator,args: list):
    if not os.path.isfile(file_name):
        print("File does not exist")
        return
    # args format = [file_name, -f, file_name, -i (optional), include_file_name (optional)]
    # -f = file to use
    # -i = include file

    # if -i is in args, then include the file
    if "-i" in args:
        include_file_name = args[args.index("-i") + 1]
        if not os.path.isfile(include_file_name):
            print("Include file does not exist")
            return
        with open(include_file_name, "r") as f:
            include_file = f.read()
        tokens = lexer_class.tokenize(include_file)
        ast = parser_class.parse_program(tokens)
        e.execute(ast)
    with open(file_name, "r") as f:

        program = f.read()
    tokens = lexer_class.tokenize(program)
    ast = parser_class.parse_program(tokens)
    e.execute(ast)
def use_as_repl(e: evaluator.Evaluator):
    while True:
        program = input(">>> ")
        if program == "quit()":
            break
        try:
            tokens = lexer_class.tokenize(program)
            ast = parser_class.parse_program(tokens)
            e.execute(ast)
        except Exception as ex:
            print(ex)

def main():
    REPL_MODE = False
    ev = evaluator.Evaluator()
    if len(sys.argv) > 1:
        if sys.argv[1] == "-r":
            REPL_MODE = True
        elif sys.argv[1] == "-f":
            use_file(sys.argv[2], ev, sys.argv)
            return
    else: 
        REPL_MODE = True
    if REPL_MODE: use_as_repl(ev)
    


if __name__ == "__main__":
    main()

