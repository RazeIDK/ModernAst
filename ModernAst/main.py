import os
import TokenMgr # Менеджер токенов

source = """
def aa(dd : bool = True):
    print(dd)
"""

def main():
    mgr = TokenMgr.Manager(source)

    print("tokens: ")
    mgr.print_tokens()




if __name__ == "__main__":
    main()
