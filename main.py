import re
import os
import sys
import openai
import asyncio

tokens = []

async def check():
    valid_tokens = ''
    valid_tokens_count = 0
    invalid_tokens = ''
    invalid_tokens_count = 0
    for token in tokens:
        openai.api_key = token
        try:
            response = await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo",
                max_tokens=20,
                temperature=0.5,
                messages=[{"role": "user", "content": 'Print "OK!"'}])
            print(f"{token} : {response['choices'][0]['message']['content']}")
            valid_tokens += f'{token}\n'
            valid_tokens_count += 1
            await asyncio.sleep(3)
        except Exception as e:
            print(f'\n{token} : {e}\n')
            invalid_tokens += f'{token} : {e}\n'
            invalid_tokens_count +=1
            await asyncio.sleep(3)

    with open("output/valid.txt", 'w', encoding="utf-8") as file:
            file.write(valid_tokens)
    with open("output/invalid.txt", 'w', encoding="utf-8") as file:
            file.write(invalid_tokens)

    print('\n\n')
    if valid_tokens_count != 0:
        print(f'Записал {valid_tokens_count} валидных токенов в файл output/valid.txt!')
    if invalid_tokens_count != 0:
        print(f'Записал {invalid_tokens_count} валидных токенов в файл output/invalid.txt!')
    print('\nЗавершаю работу!')
    await asyncio.wait(3)
    sys.exit()
    

if not os.path.isfile("tokens.txt"):
    print('Не вижу файла tokens.txt, завершаю работу!')
    asyncio.wait(3)
    sys.exit()
else:
    with open('tokens.txt', 'r', encoding='utf-8') as file:
        for line in file:
            tokens.append(re.sub('\n', '', line))
        print(f'\nЗагрузил {len(tokens)} токенов!\nНачинаю проверку...\n\n')

    if not os.path.exists("output"):
        os.mkdir("output")
    with open("output/valid.txt", 'w', encoding="utf-8") as file:
            file.write('')
    with open("output/invalid.txt", 'w', encoding="utf-8") as file:
            file.write('')

    asyncio.run(check())




