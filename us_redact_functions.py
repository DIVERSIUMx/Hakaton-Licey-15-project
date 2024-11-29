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

us_functions = {
    "pub_user_change_name":us_change_name,
    "pub_user_change_body":us_change_body,
    "pub_user_change_img":us_change_img
}
