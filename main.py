import asyncio
import logging
import sys
from os import getenv
from config import TOKEN

from aiogram import Bot, Dispatcher, html, F
from aiogram.utils.keyboard import *
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    bilder = InlineKeyboardBuilder()
    bilder.add(InlineKeyboardButton(text="Сборник", callback_data="go_to_test"))
    await message.answer(f"Hello, <b>{message.from_user.full_name}</b>", reply_markup=bilder.as_markup())


@dp.callback_query(F.data == "go_to_test")
async def send_random_value(callback: CallbackQuery):
    await callback.message.answer("ehd")
    await callback.answer()

@dp.message()
async def echo_handler(message: Message) -> None:
    try:
        # Send a copy of the received message
        if message.text == "Дурак":
            await message.answer("Сам такой!!!!!!")
    except TypeError:
        # But not all the types is supported to be copied so need to handle it
        await message.answer("Nice try!")



async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())