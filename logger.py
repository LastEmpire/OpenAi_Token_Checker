import datetime
from colorama import Fore, Style, Back

# Логгирование в консоль и файл
def log(log_path, text, color='white'):
    current_time = datetime.datetime.now().strftime(f"[%Y-%m-%d][%H:%M:%S]")

    if color == 'error':
        colored_text = Back.RED + text + Style.RESET_ALL
    elif color == 'succes':
        colored_text = Back.GREEN + text + Style.RESET_ALL
    else:
        colored_text = Fore.WHITE + text + Style.RESET_ALL

    console_string = f'{Fore.LIGHTCYAN_EX}{current_time}{Style.RESET_ALL} > {colored_text}'
    file_string = f'{current_time} > {text}'

    print(console_string)

    with open(log_path, 'a') as log_file:
        log_file.write(f'{file_string}\n')