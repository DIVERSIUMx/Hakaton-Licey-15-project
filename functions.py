from imports import *

class Functions:


    async def go_to_storage(self=None, callback=None):
        await callback.message.answer("<b>Вы</b> в сборнике")
        await callback.answer()

    async def go_to_profile(self=None, callback=None):
        user = CUR.execute(f"SELECT * FROM users WHERE telegram_id={callback.from_user.id}").fetchall()
        if len(user) == 0:
            CUR.execute(f"INSERT INTO users(telegram_id) VALUES({callback.from_user.id})")
            CON.commit()
        user = CUR.execute(f"SELECT * FROM users WHERE telegram_id={callback.from_user.id}").fetchall()[0]
        await callback.message.answer(f"{callback.from_user.full_name} \n Ваш баланс: {user[2]}")
        await callback.answer()

    functions = {
        "go_to_storage":go_to_storage,
        "go_to_profile":go_to_profile
    }