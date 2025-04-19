import asyncio
from threading import Thread
from src.backend import app
from src.bot import main as run_bot


def run_flask():
    app.run(debug=True,
            use_reloader=False)


def run_telegram_bot():
    asyncio.run(run_bot())


def main():
    bot_thread = Thread(target=run_telegram_bot, daemon=True)
    bot_thread.start()

    run_flask()


if __name__ == "__main__":
    main()
