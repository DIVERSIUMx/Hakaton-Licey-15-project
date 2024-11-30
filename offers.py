from imports import *

async def offer_promocode(callback: CallbackQuery):
    balance = CUR.execute(f"SELECT balance FROM users WHERE telegram_id={callback.from_user.id}").fetchall()[0][0]
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="⬅️ Назад", callback_data="go_to_market"))
    if balance >= 1000:
        CUR.execute(f"UPDATE users SET balance=balance-1000 WHERE telegram_id={callback.from_user.id}")
        CON.commit()
        await callback.message.answer("Покупка прошла успешно, ваш промокод: <b>KOD15</b>", reply_markup=builder.as_markup())
    else:
        await callback.message.answer("У вас не хватает баллов 😓", reply_markup=builder.as_markup())
    await callback.answer()



offers = {
    "offer_promocode":offer_promocode
}