from imports import *
import functions

@dp.message(CommandStart())
async def starter(message: Message) -> None:
    bilder = InlineKeyboardBuilder()
    bilder.row(InlineKeyboardButton(text="Сборник 📕", callback_data="go_to_storage"))
    bilder.row(InlineKeyboardButton(text="Профиль 🕵️‍", callback_data="go_to_profile"))
    bilder.row(InlineKeyboardButton(text="Маркет 🏪", callback_data="go_to_market"))

    await message.answer(f"Привет, <b>{message.from_user.full_name}</b>", reply_markup=bilder.as_markup())

@dp.callback_query(F.data.startswith("go_to_"))
async def go_to_profile(callback: CallbackQuery, bot: Bot):
    print(bot)
    await functions.functions[callback.data](callback=callback)

@dp.message()
async def echo_handler(message: Message) -> None:
    pass



async def main():
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())