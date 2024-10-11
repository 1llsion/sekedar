from colorama import Fore, Style, init
from datetime import datetime

init()

# Colors

green = f"{Fore.LIGHTGREEN_EX}"
magenta= f"{Fore.LIGHTMAGENTA_EX}"
blue = f"{Fore.LIGHTBLUE_EX}"
white = f"{Fore.LIGHTWHITE_EX}"
black = f"{Fore.LIGHTBLACK_EX}"
red =  f"{Fore.RED}"
# Info intuk output (Hasil Dari Scanner) dan untuk time now

now = datetime.now()

info = f"{white}[{blue}INFO{white}]{now.strftime(f"{white}[{magenta}%H:%M:%S{white}]")}"
vuln = f"{white}[{green}VULN{white}]{now.strftime(f"{white}[{magenta}%H:%M:%S{white}]")}"
error = f"{white}[{red}ERROR{white}]{now.strftime(f"{white}[{magenta}%H:%M:%S{white}]")}"
warn = f"{white}[{red}WARNING{white}]{now.strftime(f"{white}[{magenta}%H:%M:%S{white}]")}"
fail = f"{white}[{red}FAILED{white}]{now.strftime(f"{white}[{magenta}%H:%M:%S{white}]")}"
suc = f"{white}[{green}SUCCESS{white}]{now.strftime(f"{white}[{magenta}%H:%M:%S{white}]")}"

