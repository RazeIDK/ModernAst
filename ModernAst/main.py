import os
import TokenMgr # Менеджер токенов
import parser

source = """
if True == True:
    pass
elif True == False:
    pass
else:
    pass
"""

def main():
    mgr = TokenMgr.Manager(source)

    print("tokens: ")
    #mgr.print_tokens()

    parse = parser.AstBuilder(mgr.tokens_list)
    parse.traverse()

if __name__ == "__main__":
    main()
