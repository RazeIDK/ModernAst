import os
import TokenMgr # Менеджер токенов
import parser

source = """
def gg():
    def nn():
        pass
    def jj():
        pass

def hh():
    pass
"""

def main():
    mgr = TokenMgr.Manager(source)

    print("tokens: ")
    mgr.print_tokens()

    parse = parser.ControlFlowGraph(mgr.tokens_list)
    parse.traverse()

    print(mgr.tokenize_str())


if __name__ == "__main__":
    main()
