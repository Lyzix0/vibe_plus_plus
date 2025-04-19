import asyncio
from threading import Thread

from src.bot import main as run_bot


async def run_telegram_bot():
    await run_bot()


def main():
    asyncio.run(run_telegram_bot())


if __name__ == "__main__":
    main()
