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
    bilder.row(InlineKeyboardButton(text="Сборник 📕", callback_data="go_to_storage"),
               InlineKeyboardButton(text="Профиль", callback_data="go_to_profile"),
               InlineKeyboardButton(text="Маркет", callback_data="go_to_market")
               )
    await message.answer(f"Привет, <b>{message.from_user.full_name}</b>", reply_markup=bilder.as_markup())


@dp.callback_query(F.data == "go_to_storage")
async def send_random_value(callback: CallbackQuery):
    await callback.message.answer("<b>Вы</b> в сборнике")
    await callback.answer()

@dp.message()
async def echo_handler(message: Message) -> None:
    pass



async def main():
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())