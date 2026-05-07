import os
import TokenMgr # Менеджер токенов
import parser

source = """
import os

def main():
    if True == True:
        os.getpid()

if __name__ == '__main__':
    main()
"""

def main():
    mgr = TokenMgr.Manager(source)

    print("tokens: ")
    mgr.print_tokens()

    parse = parser.AstBuilder(mgr.tokens_list)
    parse.traverse()

if __name__ == "__main__":
    main()
