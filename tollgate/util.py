import colorama
colorama.init()

def color_print(text, color):
    print(color + text)
    print(Fore.RESET + Back.RESET + Style.RESET_ALL)

def error_print(text):
    color_print(text, Fore.RED)

def ok_print(text):
    color_print(text, Fore.GREEN)

def info_print(text):
    color_print(text, Fore.BLUE)
