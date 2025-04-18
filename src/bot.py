import os

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from dotenv import load_dotenv
import logging
from src.database import add_user
from aiogram.filters import Command


load_dotenv()
bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
logging.basicConfig(level=logging.INFO)

dp = Dispatcher()
bot = Bot(token=bot_token)


@dp.message(Command('start'))
async def start(message: Message) -> None:
    await message.reply("ПРИВЕТ!")


async def main() -> None:
    await dp.start_polling(bot)
