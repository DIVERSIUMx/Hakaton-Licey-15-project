from imports import *

async def go_to_home(callback: CallbackQuery) -> None:
    bilder = InlineKeyboardBuilder()
    bilder.row(InlineKeyboardButton(text="Сборник 📕", callback_data="go_to_storage"))
    bilder.row(InlineKeyboardButton(text="Профиль 🕵️‍", callback_data="go_to_profile"))
    bilder.row(InlineKeyboardButton(text="Маркет 🏪", callback_data="go_to_market"))

    await callback.message.answer(f"Привет, <b>{callback.from_user.full_name}</b>", reply_markup=bilder.as_markup())
    await callback.answer()


async def go_to_storage(callback=None):
    await callback.message.answer("<b>Вы</b> в сборнике")
    await callback.answer()


async def go_to_profile(callback=None):
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Назад 🔙", callback_data="go_to_home"))
    user = CUR.execute(f"SELECT * FROM users WHERE telegram_id={callback.from_user.id}").fetchall()
    if len(user) == 0:
        CUR.execute(f"INSERT INTO users(telegram_id) VALUES({callback.from_user.id})")
        CON.commit()
    user = CUR.execute(f"SELECT * FROM users WHERE telegram_id={callback.from_user.id}").fetchall()[0]
    await callback.message.answer(f"{callback.from_user.full_name} \n Ваш баланс: {user[2]}", reply_markup=builder.as_markup())
    await callback.answer()


async def go_to_market(callback: CallbackQuery):
    await callback.message.answer("Вы в маркете")
    await  callback.answer()


functions = {
    "go_to_home":go_to_home,
    "go_to_storage":go_to_storage,
    "go_to_profile":go_to_profile,
    "go_to_market":go_to_market
}
