import contextlib

import us_redact_functions
from imports import *
import functions
import moderate_functions

@dp.message(CommandStart())
async def starter(message: Message, bot: Bot) -> None:

    bilder = InlineKeyboardBuilder()
    bilder.row(InlineKeyboardButton(text="📕 Сборники", callback_data="go_to_storage"))
    bilder.row(InlineKeyboardButton(text="🕵️‍ Профиль", callback_data="go_to_profile"))
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

@dp.callback_query(F.data.startswith("pub_user_change_"))
async def pub_user_change(callback: CallbackQuery):
    await us_redact_functions.us_functions[callback.data](callback)


@dp.callback_query(F.data.startswith("moderate_publish_"))
async def moderate_publish(callback: CallbackQuery):
    id = callback.data.lstrip("moderate_publish_")
    content = CUR.execute(f"SELECT * FROM checking WHERE id={id}").fetchall()[0]
    if content[1] == "fact":
        CUR.execute(f"INSERT INTO facts(name, body, img_path) VALUES('{content[2]}', '{content[3]}', '{content[4]}')")
        if content[4] != "default.png":
            shutil.move(f"assets/photos/requests_photos/{content[4]}", f"assets/photos/facts_photos/{content[4]}")
        CUR.execute(f"DELETE FROM checking WHERE id={id}")
        CON.commit()
    else:
        CUR.execute(f"INSERT INTO places(name, body, img_path) VALUES('{content[2]}', '{content[3]}', '{content[4]}')")
        if content[4] != "default.png":
            shutil.move(f"assets/photos/requests_photos/{content[4]}", f"assets/photos/places_photos/{content[4]}")
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

@dp.callback_query(F.data.startswith("task_"))
async def task(callback: CallbackQuery):
    id = callback.data.lstrip("task_")
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="✅ Выполнить", callback_data=f"make_task_{id}"))
    builder.row(InlineKeyboardButton(text="⬅️ Назад", callback_data="go_to_tasks"))
    print(id)
    sql = f'SELECT * FROM tasks WHERE id={id}'
    print(sql)
    await callback.message.answer(f"Вы перешли к выполнению задания: {CUR.execute(sql).fetchall()[0][1]}", reply_markup=builder.as_markup())
    await callback.answer()


@dp.callback_query(F.data.startswith("make_task_"))
async def make_task(callback: CallbackQuery):
    id = callback.data.lstrip("make_task_")
    task = CUR.execute(f'SELECT * FROM tasks WHERE id={id}').fetchall()[0]
    blacklist = task[2].split(";")
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="⬅️ Назад", callback_data="go_to_tasks"))
    if str(callback.from_user.id) not in blacklist:
        blacklist.append(str(callback.from_user.id))
        CUR.execute(f"UPDATE users SET balance=balance+{task[3]}")
        CUR.execute(f"UPDATE tasks SET users='{';'.join(blacklist)}'")
        await callback.message.answer(f"Вы выполнили задание!", reply_markup=builder.as_markup())
    else:
        await callback.message.answer(f"Вы уже выполнили задание 😡!", reply_markup=builder.as_markup())



@dp.message(F.photo)
async def photo_filter(message: Message):
    if message.from_user.id in User_publish_img_redact:
        CUR.execute("UPDATE states SET value=value+1 WHERE type='max_img'")
        CON.commit()
        file_num = CUR.execute("SELECT value FROM states WHERE type='max_img'").fetchall()[0][0]
        print(file_num)
        await message.bot.download(file=message.photo[-1].file_id, destination=f"assets/photos/requests_photos/request-photo-n{file_num}.png")
        User_publish_redact[message.from_user.id][2] = f"request-photo-n{file_num}.png"
        User_publish_img_redact.remove(message.from_user.id)
        await functions.go_to_redact_user_publish_from_message(message)



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
    elif user_id in Moderator_body_redact.keys():
        CUR.execute(f"UPDATE checking SET body='{message.text}' WHERE id={Moderator_body_redact[user_id]}")
        CON.commit()
        await moderate_functions.moderate_from_message(message, Moderator_body_redact[user_id])
        Moderator_body_redact.pop(user_id)
    elif user_id in User_publish_name_redact:
        User_publish_redact[user_id][0] = message.text
        User_publish_name_redact.remove(user_id)
        await functions.go_to_redact_user_publish_from_message(message)
    elif user_id in User_publish_body_redact:
        User_publish_redact[user_id][1] = message.text
        User_publish_body_redact.remove(user_id)
        await functions.go_to_redact_user_publish_from_message(message)
    elif user_id in User_publish_img_redact:
        await message.answer("Пришлите боту жеелаемое <b>Фото</b>")




async def main():
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())