import os
import requests
import asyncio
from aiogram import Bot, Dispatcher, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, FSInputFile, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from dotenv import load_dotenv
import logging
import src.database
import src.gpt
from aiogram.filters import Command

load_dotenv()
bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
logging.basicConfig(level=logging.INFO)

HTTP_SERVER = "http://127.0.0.1:5000"
dp = Dispatcher()
bot = Bot(token=bot_token)

router = Router()


def get_main_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="Узнать время на задания"))
    return builder.as_markup(resize_keyboard=True)


# Состояния для регистрации
class RegistrationStates(StatesGroup):
    almost_reg = State()
    reg = State()


@dp.message(Command('start'))
async def start(message: Message, state: FSMContext) -> None:
    if src.database.user_data(message.from_user.id):
        await message.reply("Привет! Можете пользоваться ботом.",
                            reply_markup=get_main_keyboard())
        await state.set_state(RegistrationStates.reg)
    else:
        await message.reply("Введите свое имя и фамилию для завершения регистрации. ТЕСТОВОЕ ИМЯ: Серега Пират")
        await state.set_state(RegistrationStates.almost_reg)


@router.message(RegistrationStates.almost_reg, F.text)
async def handle_register(message: Message, state: FSMContext) -> None:
    data = requests.get(f'{HTTP_SERVER}/users').json()
    ans = False
    for x in data:
        if message.text.lower() == x['name'].lower():
            ans = True
            break

    if ans:
        await message.reply("Успешная регистрация! Можете пользоваться ботом",
                            reply_markup=get_main_keyboard())

        src.database.add_user(message.from_user.id, message.text.lower())
        await state.set_state(RegistrationStates.reg)
        return

    await message.reply("Неправильно имя! Попробуйте еще раз")


@router.message(F.text)
async def send_data(message: Message, state: FSMContext) -> None:
    if await state.get_state() == RegistrationStates.reg or src.database.user_data(message.from_user.id):
        user_name = src.database.user_data(message.from_user.id)[1]
        data = requests.get(f'{HTTP_SERVER}/users/{user_name}').json()
        marks = data['scores']['marks']

        await message.reply(f'{data['name']} - здравствуйте! Загружаю вашу информацию... Это займет немного времени...')
        message_text, image = await asyncio.gather(
            load_info(marks, data['scores']['course'], data['scores']['direction']),
            gen_homa()
        )
        image.save('name.png')

        await bot.send_photo(message.from_user.id, parse_mode='Markdown', photo=FSInputFile('name.png'),
                             caption=message_text,
                             reply_markup=get_main_keyboard())
    else:
        await start(message, state)


async def load_info(marks, course, direction):
    gen = src.gpt.Generator()
    await gen.load_sdk_text()
    data = requests.get(f'{HTTP_SERVER}/course_{course}/{direction}').json()

    tasks = [gen.gen_summary(f'{marks}   {x["description"]}') for x in data['tasks']]
    texts = await asyncio.gather(*tasks, return_exceptions=True)

    message = format_marks(marks) + '\n\n'
    for a, text in zip(data['tasks'], texts):
        message += f'*{a['title']}*: \n{a['description']} \n\n{text}\n\n'

    return message


async def gen_homa():
    gen = src.gpt.Generator()
    await gen.load_sdk_image()
    image = await gen.gen_image("Веселый хомячок хома в стиле комикс")
    return image


dp.include_router(router)


def format_marks(marks: dict) -> str:
    marks_text = "📊 *Ваши текущие оценки:*\n"
    marks_text += "| Предмет  | Оценка |\n"
    for subject, grade in marks.items():
        marks_text += f"{subject.capitalize()} {grade}\n"
    return marks_text


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
