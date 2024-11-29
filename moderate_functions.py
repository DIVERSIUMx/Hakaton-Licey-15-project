import functions
from imports import *

async def moderate(callback: CallbackQuery):
    id = callback.data.lstrip("moderate_content_")
    content = CUR.execute(f"SELECT * FROM checking WHERE id={id}").fetchall()[0]
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="✏️ Изменить название", callback_data=f"moderate_change_name_{id}"), InlineKeyboardButton(text="✏️ Изменить содержание", callback_data=f"moderate_change_body_{id}"))
    builder.row(InlineKeyboardButton(text="✅ Опубликовать", callback_data=f"moderate_publish_{id}"), InlineKeyboardButton(text="❌ Отклонить", callback_data=f"moderate_discard_{id}"), InlineKeyboardButton(text="⬅️ Отмена", callback_data=f"go_to_requests"))
    await callback.bot.send_photo(callback.message.chat.id, photo=FSInputFile(f"assets/photos/requests_photos/{content[4]}"),
                                  caption=f"<b>{content[2]}</b>\n{content[3]}", reply_markup=builder.as_markup())
    await callback.answer()


async def moderate_from_message(message: Message, id:int):
    content = CUR.execute(f"SELECT * FROM checking WHERE id={id}").fetchall()[0]
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="✏️ Изменить название", callback_data=f"moderate_change_name_{id}"), InlineKeyboardButton(text="✏️ Изменить содержание", callback_data=f"moderate_change_body_{id}"))
    builder.row(InlineKeyboardButton(text="✅ Опубликовать", callback_data=f"moderate_publish_{id}"), InlineKeyboardButton(text="❌ Отклонить", callback_data=f"moderate_publish_{id}"), InlineKeyboardButton(text="⬅️ Отмена", callback_data=f"go_to_requests"))
    await message.bot.send_photo(message.chat.id, photo=FSInputFile(f"assets/photos/requests_photos/{content[4]}"),
                                  caption=f"<b>{content[2]}</b>\n{content[3]}", reply_markup=builder.as_markup())
    print("wrgewbiguewpiufewofb")

async def moderate_change_name(callback: CallbackQuery):
    Moderator_name_redact[callback.from_user.id] = callback.data.lstrip("moderate_change_name_")
    print(Moderator_name_redact)
    await callback.message.answer("Введите новое имя публикации и отправте мне:")
    await callback.answer()


async def moderate_change_body(callback: CallbackQuery):
    Moderator_body_redact[callback.from_user.id] = callback.data.lstrip("moderate_change_body_")
    print(Moderator_name_redact)
    await callback.message.answer("Введите новое имя публикации и отправте мне:")
    await callback.answer()

