import re
import os
import sys
import openai
import asyncio
import datetime
import shutil
from logger import log
from colorama import Fore, Style

# Глобальные переменные
VERSION = 3.0

LOGO = f"""
{Fore.LIGHTBLUE_EX}   ___                      _    ___   _____     _              
  / _ \ _ __   ___ _ __    / \  |_ _| |_   _|__ | | _____ _ __  
 | | | | '_ \ / _ \ '_ \  / _ \  | |    | |/ _ \| |/ / _ \ '_ \ 
 | |_| | |_) |  __/ | | |/ ___ \ | |    | | (_) |   <  __/ | | |
  \___/| .__/ \___|_|{Fore.LIGHTGREEN_EX}_{Fore.LIGHTBLUE_EX}|_/_/   \_\___|{Fore.LIGHTGREEN_EX}_{Fore.LIGHTBLUE_EX}  |_|\___/|_|\_\___|_| |_|
       |_|     {Fore.LIGHTGREEN_EX}/ ___| |__   ___  ___| | _____ _ __              
              | |   | '_ \ / _ \/ __| |/ / _ \ '__|             
              | |___| | | |  __/ (__|   <  __/ |                
               \____|_| |_|\___|\___|_|\_\___|_|

{Fore.BLUE}({VERSION}) By Lemarty{Style.RESET_ALL}
"""

tokens = []

pattern = r'sk-[A-Za-z0-9]{20}T3BlbkFJ[A-Za-z0-9]{20}'


# Функция проверки токенов через API запросы
async def check_tokens() -> None:

    valid_tokens = ''
    valid_tokens_count = 0
    invalid_tokens = ''
    invalid_tokens_count = 0
    checker_count = 0

    for token in tokens:
        checker_count += 1
        openai.api_key = token
        try:
            # Отправка запроса
            response = await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo",
                max_tokens=10,
                temperature=0.1,
                messages=[{"role": "user", "content": 'Print "OK!"'}])
            log(LOG_PATH, f"{checker_count} : {token} : {response['choices'][0]['message']['content']}", 'succes')
            valid_tokens += f'{token}\n'
            valid_tokens_count += 1
        
        except Exception as error:
            # При получении ошибки
            log(LOG_PATH, f'{checker_count} : {token} : {error}', 'error')
            invalid_tokens += f'{token} : {error}\n'
            invalid_tokens_count += 1
        await asyncio.sleep(1)

    # Создание директорий
    if not os.path.exists("output"):
        os.mkdir("output")
    shutil.copy(tokens_file, f"cahce/{now}/")
    print("")

    # Запись валидных и невалидных токенов в соответствующие файлы
    if valid_tokens_count:
        with open("output/valid.txt", 'w', encoding="utf-8") as file:
            file.write(valid_tokens)
        with open(f"cahce/{now}/valid.txt", 'w', encoding="utf-8") as file:
            file.write(valid_tokens)
        log(LOG_PATH, f'Записал {valid_tokens_count} валидных токенов в файл output/valid.txt!')

    if invalid_tokens_count:
        with open("output/invalid.txt", 'w', encoding="utf-8") as file:
            file.write(invalid_tokens)
        with open(f"cahce/{now}/invalid.txt", 'w', encoding="utf-8") as file:
            file.write(invalid_tokens)
        log(LOG_PATH, f'Записал {invalid_tokens_count} невалидных токенов в файл output/invalid.txt!')

    sys.exit(log(LOG_PATH, 'Завершаю работу!'))
    
# Инициализация
print(LOGO)
now = datetime.datetime.now().strftime("%H.%M.%S-%d.%m.%Y")
os.makedirs(f"cahce/{now}/")
LOG_PATH = f"cahce/{now}/log.txt"

# Поиск токенов в файле
tokens_file = None
for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.txt') and (file != 'requirements.txt'):
            tokens_file = file
    break
if not tokens_file:
    sys.exit(log(LOG_PATH, 'Не вижу текстового файла в директории, завершаю работу!', 'error'))
else:
    log(LOG_PATH, f"Читаю файл {tokens_file}...")
    with open(tokens_file, 'r', encoding='utf-8') as file:
        lines = file.read()
        matches = re.findall(pattern, lines)
        for match in matches:
            if match not in tokens:
                tokens.append(match)
        if tokens:
            log(LOG_PATH, f'Загрузил {len(tokens)} токенов! Начинаю проверку...')
            print("")
        else:
            sys.exit(log(LOG_PATH, 'В файле текстовом файле нет токенов, соответствующих формату, завершаю работу!', 'error'))

    # Запуск проверки
    asyncio.run(check_tokens())




