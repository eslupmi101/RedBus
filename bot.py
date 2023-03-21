import json
import logging
import os


from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv


load_dotenv()


API_TOKEN = os.getenv("TOKEN")


logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


OTHER_COMMANDS = ['урод', 'красный', 'удалить']


def get_db() -> None:
    with open('db.json') as json_file:
        data = json.load(json_file)
    return data


def update_db(command_bot: str, bus_number: str):
    data = get_db()
    if command_bot == 'какой автобус':
        if bus_number not in data:
            return "Автобуса нет в базе"
        else:
            if str(data[bus_number]).lower() == 'красный':
                return "Это КЛАСНЫЙ!!! СУПЕЛЛЛ"
            elif str(data[bus_number]).lower() == 'урод':
                return "Нееееет! Это УЛООООД"
    elif command_bot == 'урод':
        data[bus_number] = 'урод'
    elif command_bot == 'красный':
        data[bus_number] = 'красный'
    elif command_bot == 'удалить':
        del data[bus_number]
    safe_db(data)
    return "База обновлена"


def safe_db(data: dict):
    with open('db.json', 'w') as outfile:
        json.dump(data, outfile)


@dp.message_handler(commands='start')
async def send_welcome(message: types.Message):
    answer = ("Здесь можно узнать приедет ли к вам:\n"
              "Красный автобус или Урод\n"
              "Введите номер автобуса")
    await message.reply(answer)


@dp.message_handler(commands='help')
async def send_help(message: types.Message):
    answer = ("Напишите, чтобы добавить в базу автобус\n"
              "Красный НОМЕРАВТОБУСА\n"
              "Урод НОМЕРАВТОБУСА\n"
              "Удалить НОМЕРАВТОБУСА")
    await message.reply(answer)


@dp.message_handler()
async def echo(message: types.Message):
    try:
        answer: str = ''
        request = message.text.split(' ')
        if (len(request) == 1
           and request[0].isdigit()):
            answer = update_db("какой автобус", str(request[0]))
        elif (len(request) != 2
              or request[0].lower() not in OTHER_COMMANDS
              or not request[1].isdigit()):
            await message.answer("Неверная команда")
        else:
            answer = update_db(request[0].lower(), str(request[1]))
    except:
        await message.answer("Неверная команда")
    else:
        await message.answer(answer)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)