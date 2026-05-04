import os
import TokenMgr # Менеджер токенов
import parser

source = """
def gg():
    pass
"""

def main():
    mgr = TokenMgr.Manager(source)

    print("tokens: ")
    mgr.print_tokens()

    parse = parser.ControlFlowGraph(mgr.tokens_list)
    parse.analyze()

    print(mgr.tokenize_str())


if __name__ == "__main__":
    main()
