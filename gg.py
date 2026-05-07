import os

def main():
    if os.name != 'nt':
        os.getpid()

if __name__ == '__main__':
    main()