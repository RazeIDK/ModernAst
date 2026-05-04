import os
import TokenMgr # Менеджер токенов
import cfg

source = """
f = 10 + 0
"""

def main():
    mgr = TokenMgr.Manager(source)

    print("tokens: ")
    mgr.print_tokens()

    CFG = cfg.ControlFlowGraph(mgr.tokens_list)
    CFG.analyze()


if __name__ == "__main__":
    main()
