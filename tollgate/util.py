import colorama
colorama.init()

def color_print(text, color):
    print(color + text)
    print(colorama.Fore.RESET + colorama.Back.RESET + colorama.Style.RESET_ALL)

def error_print(text):
    color_print(text, colorama.Fore.RED)

def ok_print(text):
    color_print(text, colorama.Fore.GREEN)

def info_print(text):
    color_print(text, colorama.Fore.BLUE)
