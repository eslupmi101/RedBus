import json
import logging
import os


from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("TOKEN")

logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

OTHER_COMMANDS = ['урод', 'красный', 'удалить', 'Красные', 'Уроды']

keyboard = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
button_red = KeyboardButton('Красные')
button_weird = KeyboardButton('Уроды')

# Добавляем кнопки на клавиатуру
keyboard.add(button_red, button_weird)


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
    await message.reply(answer, reply_markup=keyboard)


@dp.message_handler(commands='help')
async def send_help(message: types.Message):
    answer = ("Напишите, чтобы добавить в базу автобус\n"
              "Красный НОМЕРАВТОБУСА\n"
              "Урод НОМЕРАВТОБУСА\n"
              "Удалить НОМЕРАВТОБУСА")
    await message.reply(answer, reply_markup=keyboard)


@dp.message_handler(
    lambda message: message.text not in ['Красные', 'Уроды']
)
async def echo(message: types.Message):
    answer: str = ''
    request = message.text.split(' ')
    if (
        len(request) == 1
        and request[0].isdigit()
    ):
        answer = update_db("какой автобус", str(request[0]))
        await message.answer(answer, reply_markup=keyboard)
    elif (
        request[0].lower() in ["красный", "урод", "удалить"]
    ):
        answer = update_db(request[0].lower(), str(request[1]))
        await message.answer(answer, reply_markup=keyboard)
    elif (
        str(request[0]) not in OTHER_COMMANDS
    ):
        await message.answer("Неверная команда", reply_markup=keyboard)


@dp.message_handler(lambda message: message.text == 'Красные')
async def red_button_handler(message: types.Message):
    db = get_db()
    answer: str = "Красные автобусы:\n"
    for number, value in db.items():
        if db[number] == "красный":
            answer += f"{number}\n"

    await message.answer(answer, reply_markup=keyboard)


@dp.message_handler(lambda message: message.text == 'Уроды')
async def weird_button_handler(message: types.Message):
    db = get_db()
    answer: str = "Уроды:\n"
    for number, value in db.items():
        if db[number] == "урод":
            answer += f"{number}\n"

    await message.answer(answer, reply_markup=keyboard)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
