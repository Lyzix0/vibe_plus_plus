import asyncio
import os

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from dotenv import load_dotenv
import logging


load_dotenv()
bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
logging.basicConfig(level=logging.INFO)

dp = Dispatcher()
bot = Bot(token=bot_token)


@dp.message()
async def summary_message(message: Message) -> None:
    await message.reply('42')


async def main() -> None:
    await dp.start_polling(bot)