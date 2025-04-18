import os

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


@dp.message(Command('start'))
async def start(message: Message, state: FSMContext) -> None:
    if src.database.has_user(message.from_user.id):
        await message.reply("ПРИВЕТ!")
    else:
        await message.reply("ВВЕДИТЕ СВОЕ ИМЯ И ФАМИЛИЮ ДЛЯ ЗАВЕРШЕНИЯ РЕГИСТРАЦИИ")
        await state.set_state(RegistrationStates.almost_reg)


@router.message(RegistrationStates.almost_reg, F.text)
async def handle_register(message: Message) -> None:
    await message.reply('ты гей')


dp.include_router(router)


async def main() -> None:
    await dp.start_polling(bot)
