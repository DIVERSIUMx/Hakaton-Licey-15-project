import functions
from imports import *

async def us_change_name(callback: CallbackQuery):
    await callback.message.answer(f"Введите новое название публикации:")
    await callback.answer()
    User_publish_name_redact.append(callback.from_user.id)

async def us_change_body(callback: CallbackQuery):
    await callback.message.answer(f"Введите новое содержание публикации:")
    await callback.answer()
    User_publish_body_redact.append(callback.from_user.id)


async def us_change_img(callback: CallbackQuery):
    await callback.message.answer(f"Пришлите сюда новое фото публикации:")
    await callback.answer()
    User_publish_img_redact.append(callback.from_user.id)


async def us_change_type(callback: CallbackQuery):
    User_publish_redact[callback.from_user.id][3] = {"fact":"place", "place":"fact"}[User_publish_redact[callback.from_user.id][3]]
    #await callback.bot.delete_message(callback.message.chat.id, callback.message.message_id)
    await functions.go_to_redact_user_publish(callback)


async def us_publish(callback: CallbackQuery):
    content = User_publish_redact[callback.from_user.id]
    print("wefwefwf")
    CUR.execute(f"INSERT INTO checking(type, name, body, img_path) VALUES('{content[3]}','{content[0]}','{content[2]}','{content[2]}')")
    CON.commit()
    await callback.answer()
    await functions.go_to_profile(callback)

us_functions = {
    "pub_user_change_name":us_change_name,
    "pub_user_change_body":us_change_body,
    "pub_user_change_img":us_change_img,
    "pub_user_change_type":us_change_type,
    "pub_user_change_publish":us_publish
}
