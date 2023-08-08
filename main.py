import re
import os
import sys
import openai
import asyncio

# Массив с токенами
tokens = []

# Глобальные переменные
valid_tokens = ''
valid_tokens_count = 0
invalid_tokens = ''
invalid_tokens_count = 0

# Паттерн проверки формата токенов
pattern = r'^sk-[A-Za-z0-9]{20}T3BlbkFJ[A-Za-z0-9]{20}$'

# Функция проверки токенов через API запросы
async def check_tokens() -> None:

    global valid_tokens, valid_tokens_count, invalid_tokens, invalid_tokens_count
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
            print(f"{checker_count} : {token} : {response['choices'][0]['message']['content']}")
            valid_tokens += f'{token}\n'
            valid_tokens_count += 1
            await asyncio.sleep(1)
        
        except Exception as error:
            # При получении ошибки
            print(f'\n{checker_count} : {token} : {error}\n')
            invalid_tokens += f'{token} : {error}\n'
            invalid_tokens_count +=1
            await asyncio.sleep(1)

    # Создание папки data
    if not os.path.exists("output"):
        os.mkdir("output")

    # Запись валидных и невалидных токенов в соответствующие файлы
    if valid_tokens_count != 0:
        with open("output/valid.txt", 'w', encoding="utf-8") as file:
            file.write(valid_tokens)
        print(f'\nЗаписал {valid_tokens_count} валидных токенов в файл output/valid.txt!')

    if invalid_tokens_count != 0:
        with open("output/invalid.txt", 'w', encoding="utf-8") as file:
            file.write(invalid_tokens)
        print(f'\nЗаписал {invalid_tokens_count} невалидных токенов в файл output/invalid.txt!')

    sys.exit('\nЗавершаю работу!')
    
# Загрузка токенов из файла, фильтрация по формату
if not os.path.isfile("tokens.txt"):
    sys.exit('Не вижу файла tokens.txt, завершаю работу!')
else:
    with open('tokens.txt', 'r', encoding='utf-8') as file:
        for line in file:
            token = re.sub('\n', '', line)
            match = re.match(pattern, token)
            if match:
                tokens.append(token)
            else:
                print(f'Токен "{token}" не соответвует формату, пропускаю!')
                invalid_tokens += f'{token} : Invalid_Format\n'
                invalid_tokens_count += 1
        if len(tokens) != 0:
            print(f'\nЗагрузил {len(tokens)} токенов!\nНачинаю проверку...\n\n')
        else:
            sys.exit('В файле tokens.txt нет токенов, соответствующих формату, завершаю работу!')

    # Запуск проверки
    asyncio.run(check_tokens())




