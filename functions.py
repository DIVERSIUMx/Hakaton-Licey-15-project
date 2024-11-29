from imports import *

async def go_to_home(callback: CallbackQuery) -> None:
    bilder = InlineKeyboardBuilder()
    bilder.row(InlineKeyboardButton(text="Сборники 📕", callback_data="go_to_storage"))
    bilder.row(InlineKeyboardButton(text="Профиль 🕵️‍", callback_data="go_to_profile"))
    bilder.row(InlineKeyboardButton(text="Маркет 🏪", callback_data="go_to_market"))

    await callback.bot.send_photo(callback.message.chat.id, photo=FSInputFile("assets/photos/hello.png"),
                         caption=f"Привет, <b>{callback.from_user.full_name}</b>",
                         reply_markup=bilder.as_markup())
    await callback.answer()


async def go_to_storage(callback=None):
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Сборник фактов", callback_data="go_to_facts"))
    builder.row(InlineKeyboardButton(text="⬅️ Назад", callback_data="go_to_home"))
    await callback.message.answer("Добро пожаловать в Сборник, здесь <b>Вы</b> можете подобрать для себя интересные места или узнать интересные факты", reply_markup=builder.as_markup())
    await callback.answer()


async def go_to_profile(callback=None):
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="⬅️ Назад", callback_data="go_to_home"))
    user = CUR.execute(f"SELECT * FROM users WHERE telegram_id={callback.from_user.id}").fetchall()
    if len(user) == 0:
        CUR.execute(f"INSERT INTO users(telegram_id) VALUES({callback.from_user.id})")
        CON.commit()
    user = CUR.execute(f"SELECT * FROM users WHERE telegram_id={callback.from_user.id}").fetchall()[0]
    await callback.message.answer(f"{callback.from_user.full_name} \n Ваш баланс: {user[2]}", reply_markup=builder.as_markup())
    await callback.answer()


async def go_to_market(callback: CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="⬅️ Назад", callback_data="go_to_home"))
    await callback.message.answer("Вы в маркете",  reply_markup=builder.as_markup())
    await  callback.answer()


async def go_to_facts(callback: CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="🎲 Случайный факт", callback_data="go_to_random_fact"))
    builder.row(InlineKeyboardButton(text="⬅️ Назад", callback_data="go_to_storage"))
    await callback.message.answer("Добро пожаловать в <b>сборник фактов</b>, сдесь вы можете узнать много интересных и забавных фактов о Воронежской области", reply_markup=builder.as_markup())
    await callback.answer()


async def go_to_random_fact(callback: CallbackQuery):
    builder = InlineKeyboardBuilder()
    facts = CUR.execute("SELECT * FROM facts").fetchall()
    fact = random.choice(facts)
    print(random.choice(facts))
    builder.row(InlineKeyboardButton(text="🎲 Попробывать Ещё...", callback_data="go_to_random_fact"))
    builder.row(InlineKeyboardButton(text="⬅️ Назад", callback_data="go_to_facts"))
    await callback.bot.send_photo(callback.message.chat.id, photo=FSInputFile(f"assets/photos/facts_photos/{fact[3]}"), caption=f"<b>{fact[1]}</b>\n{fact[2]}", reply_markup=builder.as_markup())
    await callback.answer()

functions = {
    "go_to_home":go_to_home,
    "go_to_storage":go_to_storage,
    "go_to_profile":go_to_profile,
    "go_to_market":go_to_market,
    "go_to_facts":go_to_facts,
    "go_to_random_fact":go_to_random_fact
}
