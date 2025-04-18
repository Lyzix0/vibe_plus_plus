import os
import requests
from aiogram import Bot, Dispatcher, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from dotenv import load_dotenv
import logging
import src.database
from aiogram.filters import Command

load_dotenv()
bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
logging.basicConfig(level=logging.INFO)

dp = Dispatcher()
bot = Bot(token=bot_token)

router = Router()


# Состояния для регистрации
class RegistrationStates(StatesGroup):
    almost_reg = State()
    reg = State()


@dp.message(Command('start'))
async def start(message: Message, state: FSMContext) -> None:
    if src.database.user_data(message.from_user.id):
        await message.reply("ПРИВЕТ!")
        await state.set_state(RegistrationStates.reg)
    else:
        await message.reply("ВВЕДИТЕ СВОЕ ИМЯ И ФАМИЛИЮ ДЛЯ ЗАВЕРШЕНИЯ РЕГИСТРАЦИИ")
        await state.set_state(RegistrationStates.almost_reg)


@router.message(RegistrationStates.almost_reg, F.text)
async def handle_register(message: Message, state: FSMContext) -> None:
    data = requests.get('http://127.0.0.1:5000/users').json()
    ans = False
    for x in data:
        if message.text.lower() == x['name'].lower():
            ans = True
            break

    if ans:
        await message.reply("ТЫ МОЛОДЕЦ ПОЛЬЗУЙСЯ БОТОМ")
        src.database.add_user(message.from_user.id, message.text.lower())
        await state.set_state(RegistrationStates.reg)
        return

    await message.reply("НЕТ ТЫ ВВЕЛ НЕ ТО ИМЯ ПРОБУЙ ЕЩЕ РАЗ")


@router.message(RegistrationStates.reg, F.text)
async def send_data(message: Message, state: FSMContext) -> None:
    user_name = src.database.user_data(message.from_user.id)[1]
    data = requests.get(f'http://127.0.0.1:5000/users/{user_name}').json()
    print(data.scores)

dp.include_router(router)


async def main() -> None:
    await dp.start_polling(bot)
