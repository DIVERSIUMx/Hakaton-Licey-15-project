from imports import *
import functions
import moderate_functions

@dp.message(CommandStart())
async def starter(message: Message, bot: Bot) -> None:

    bilder = InlineKeyboardBuilder()
    bilder.row(InlineKeyboardButton(text="Сборники 📕", callback_data="go_to_storage"))
    bilder.row(InlineKeyboardButton(text="Профиль 🕵️‍", callback_data="go_to_profile"))
    bilder.row(InlineKeyboardButton(text="Маркет 🏪", callback_data="go_to_market"))
    await bot.send_photo(message.chat.id, photo=FSInputFile("assets/photos/hello.png"),
                         caption=f"Привет, <b>{message.from_user.full_name}</b>",
                         reply_markup=bilder.as_markup())

@dp.callback_query(F.data.startswith("go_to_"))
async def go_to(callback: CallbackQuery, bot: Bot):
    print(bot)
    await functions.functions[callback.data](callback=callback)

@dp.callback_query(F.data.startswith("moderate_content_"))
async def moderate_content(callback: CallbackQuery):
    await moderate_functions.moderate(callback)

@dp.callback_query(F.data.startswith("moderate_change_name_"))
async def moderate_change_name(callback: CallbackQuery):
    await moderate_functions.moderate_change_name(callback)


@dp.callback_query(F.data.startswith("moderate_change_body_"))
async def moderate_change_name(callback: CallbackQuery):
    await moderate_functions.moderate_change_body(callback)


@dp.callback_query(F.data.startswith("moderate_publish_"))
async def moderate_publish(callback: CallbackQuery):
    id = callback.data.lstrip("moderate_publish_")
    content = CUR.execute(f"SELECT * FROM checking WHERE id={id}").fetchall()[0]
    if content[1] == "fact":
        CUR.execute(f"INSERT INTO facts(name, body, img_path) VALUES('{content[2]}', '{content[3]}', '{content[4]}')")
        CUR.execute(f"DELETE FROM checking WHERE id={id}")
        CON.commit()
    else:
        CUR.execute(f"INSERT INTO places(name, body, img_path) VALUES('{content[2]}', '{content[3]}', '{content[4]}')")
        CUR.execute(f"DELETE FROM checking WHERE id={id}")
        CON.commit()
    await callback.answer()
    await functions.functions["go_to_requests"](callback=callback)


@dp.callback_query(F.data.startswith("moderate_discard_"))
async def moderate_discard(callback: CallbackQuery):
    id = callback.data.lstrip("moderate_discard_")
    CUR.execute(f"DELETE FROM checking WHERE id={id}")
    CON.commit()
    await callback.answer()
    await functions.functions["go_to_requests"](callback=callback)

@dp.message()
async def echo_handler(message: Message) -> None:
    user_id = message.from_user.id
    print(user_id, Moderator_body_redact.keys())
    if user_id in Moderator_name_redact.keys():
        print(message.text)
        CUR.execute(f"UPDATE checking SET name='{message.text}' WHERE id={Moderator_name_redact[user_id]}")
        CON.commit()
        await moderate_functions.moderate_from_message(message, Moderator_name_redact[user_id])
        Moderator_name_redact.pop(user_id)
    if user_id in Moderator_body_redact.keys():
        CUR.execute(f"UPDATE checking SET body='{message.text}' WHERE id={Moderator_body_redact[user_id]}")
        CON.commit()
        await moderate_functions.moderate_from_message(message, Moderator_body_redact[user_id])
        Moderator_body_redact.pop(user_id)


async def main():
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())