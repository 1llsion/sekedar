from models.menu import *
from exploit.wpbf import main as wpbf
from exploit.joomla import main as bfjoomla

if __name__ == "__main__":
    menu()
    cmd = input(f"{magenta}Ethopia ==> ")
    if cmd == "1":
        wpbf()
    elif cmd == "2":
        bfjoomla()
    else:
        exit(1)