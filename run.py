import asyncio
from threading import Thread

from src.backend import app
from src.bot import main as run_bot


def run_flask():
    app.run(debug=False)


async def run_telegram_bot():
    await run_bot()


def main():
    flask_thread = Thread(target=run_flask)
    flask_thread.start()

    asyncio.run(run_telegram_bot())


if __name__ == "__main__":
    main()
