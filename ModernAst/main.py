import os
import TokenMgr # Менеджер токенов
import parser

source = """
one.five()
"""

def main():
    mgr = TokenMgr.Manager(source)

    print("tokens: ")
    #mgr.print_tokens()

    parse = parser.AstBuilder(mgr.tokens_list)
    parse.traverse()

if __name__ == "__main__":
    main()
