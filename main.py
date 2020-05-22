from ply import lex, yacc

import tokens
import grammar
import execute
import sys

def main():
    if len(sys.argv) < 2:
        print("Need argument")
        return

    lexer = lex.lex(module=tokens)
    parser = yacc.yacc(module=grammar)

    with open(sys.argv[1], "rb") as f:
        code = f.read().decode()

    print(code)
    ast = parser.parse(code)
    execute.execute(ast)

if __name__ == '__main__':
    main()
