from imports import *

async def go_to_home(callback: CallbackQuery) -> None:
    bilder = InlineKeyboardBuilder()
    bilder.row(InlineKeyboardButton(text="📕 Сборники", callback_data="go_to_storage"))
    bilder.row(InlineKeyboardButton(text="🕵️‍ Профиль", callback_data="go_to_profile"))
    bilder.row(InlineKeyboardButton(text="🏪 Маркет", callback_data="go_to_market"))

    await callback.bot.send_photo(callback.message.chat.id, photo=FSInputFile("assets/photos/hello.png"),
                         caption=f"Главное меню",
                         reply_markup=bilder.as_markup())
    await callback.answer()


async def go_to_storage(callback=None):
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="🗺️ Сборник мест", callback_data="go_to_places"))
    builder.row(InlineKeyboardButton(text="💡 Сборник фактов", callback_data="go_to_facts"))
    builder.row(InlineKeyboardButton(text="⬅️ Назад", callback_data="go_to_home"))
    await callback.bot.send_photo(callback.message.chat.id, photo=FSInputFile("assets/photos/storage.png"), caption="Добро пожаловать в Сборник, здесь <b>Вы</b> можете подобрать для себя интересные места или узнать интересные факты", reply_markup=builder.as_markup())
    await callback.answer()


async def go_to_profile(callback=None):
    builder = InlineKeyboardBuilder()

    user = CUR.execute(f"SELECT * FROM users WHERE telegram_id={callback.from_user.id}").fetchall()
    builder.row(InlineKeyboardButton(text="🔨 Предложить публикацию", callback_data="go_to_make_request"))
    if len(user) == 0:
        CUR.execute(f"INSERT INTO users(telegram_id) VALUES({callback.from_user.id})")
        CON.commit()
    user = CUR.execute(f"SELECT * FROM users WHERE telegram_id={callback.from_user.id}").fetchall()[0]
    if user[3]:
        builder.row(InlineKeyboardButton(text="❗ Входящие запросы", callback_data="go_to_requests"))
    builder.row(InlineKeyboardButton(text="⬅️ Назад", callback_data="go_to_home"))
    await callback.message.answer(f"{callback.from_user.full_name} \n Ваш баланс: {user[2]}", reply_markup=builder.as_markup())
    await callback.answer()


async def go_to_market(callback: CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="🪙 Заработать баллы", callback_data="go_to_tasks"))
    builder.row(InlineKeyboardButton(text="🛍️ К офферам", callback_data="go_to_offers"))
    builder.row(InlineKeyboardButton(text="⬅️ Назад", callback_data="go_to_home"))
    await callback.message.answer("добро пожаловать в <b>маркет</b>, здесь вы можете  заробатывать баллы, проходя разные задания и тратить их на промокоды, статусы и т. д.",  reply_markup=builder.as_markup())
    await  callback.answer()


async def go_to_facts(callback: CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="🎲 Случайный факт", callback_data="go_to_random_fact"))
    builder.row(InlineKeyboardButton(text="⬅️ Назад", callback_data="go_to_storage"))
    text = "Добро пожаловать в <b>сборник фактов</b>, здесь вы можете узнать много интересных и забавных фактов о Воронежской области"
    await callback.bot.send_photo(callback.message.chat.id, photo=FSInputFile("assets/photos/facts.png"), caption=text, reply_markup=builder.as_markup())
    await callback.answer()


async def go_to_random_fact(callback: CallbackQuery):
    builder = InlineKeyboardBuilder()
    facts = CUR.execute("SELECT * FROM facts").fetchall()
    fact = random.choice(facts)
    print(random.choice(facts))
    builder.row(InlineKeyboardButton(text="🎲 Попробовать Ещё...", callback_data="go_to_random_fact"))
    builder.row(InlineKeyboardButton(text="⬅️ Назад", callback_data="go_to_facts"))
    await callback.bot.send_photo(callback.message.chat.id, photo=FSInputFile(f"assets/photos/facts_photos/{fact[3]}"), caption=f"<b>{fact[1]}</b>\n{fact[2]}", reply_markup=builder.as_markup())
    await callback.answer()


async def go_to_places(callback: CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="🎲 Ткнуть пальцем в карту", callback_data="go_to_random_place"))
    builder.row(InlineKeyboardButton(text="⬅️ Назад", callback_data="go_to_storage"))
    text = "Добро пожаловать в <b>сборник мест</b>, здесь вы можете узнать о интересных местах Воронежской области"
    await callback.bot.send_photo(callback.message.chat.id, photo=FSInputFile("assets/photos/facts.png"), caption=text,
                                  reply_markup=builder.as_markup())
    await callback.answer()


async def go_to_random_place(callback: CallbackQuery):
    builder = InlineKeyboardBuilder()
    places = CUR.execute("SELECT * FROM places").fetchall()
    place = random.choice(places)
    builder.row(InlineKeyboardButton(text="🎲 Попробовать Ещё...", callback_data="go_to_random_place"))
    builder.row(InlineKeyboardButton(text="⬅️ Назад", callback_data="go_to_places"))
    await callback.bot.send_photo(callback.message.chat.id, photo=FSInputFile(f"assets/photos/places_photos/{place[3]}"), caption=f"<b>{place[1]}</b>\n{place[2]}", reply_markup=builder.as_markup())
    await callback.answer()


async def go_to_requests(callback: CallbackQuery):
    chat_id = callback.message.chat.id
    await callback.message.answer("Места:")
    places = CUR.execute("SELECT * FROM checking WHERE type='place'")
    for place in places:
        builder = InlineKeyboardBuilder()
        builder.add(InlineKeyboardButton(text="☝️ Перейти", callback_data=f"moderate_content_{place[0]}"))
        builder.add(InlineKeyboardButton(text="❌ Отклонить", callback_data=f"moderate_discard_{place[0]}"))
        await callback.bot.send_photo(chat_id, photo=FSInputFile(f"assets/photos/requests_photos/{place[4]}"), caption=f"<b>{place[2]}</b>\n{place[3]}", reply_markup=builder.as_markup())

    await callback.message.answer("Факты:")
    facts = CUR.execute("SELECT * FROM checking WHERE type='fact'")
    print(facts)
    for fact in facts:
        builder = InlineKeyboardBuilder()
        builder.add(InlineKeyboardButton(text="☝️ Перейти", callback_data=f"moderate_content_{fact[0]}"))
        builder.add(InlineKeyboardButton(text="❌ Отклонить", callback_data=f"moderate_discard_{fact[0]}"))
        await callback.bot.send_photo(chat_id, photo=FSInputFile(f"assets/photos/requests_photos/{fact[4]}"),
                                      caption=f"<b>{fact[2]}</b>\n{fact[3]}", reply_markup=builder.as_markup())
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="⬅️ Назад", callback_data=f"go_to_profile"))
    await callback.message.answer(text="Входящие запросы ☝️", reply_markup=builder.as_markup())
    await callback.answer()

async def go_to_make_request(callback: CallbackQuery):
    User_publish_redact[callback.from_user.id] = ["НАЗВАНИЕ", "СОДЕРЖАНИЕ", "default.png", "fact"]
    await go_to_redact_user_publish(callback)


async  def go_to_redact_user_publish(callback: CallbackQuery):
    user_redact = User_publish_redact[callback.from_user.id]
    builder = InlineKeyboardBuilder()
    type = {"fact":"факт", "place":"место"}[User_publish_redact[callback.from_user.id][3]]
    builder.row(InlineKeyboardButton(text="✏️ Изменить Название", callback_data="pub_user_change_name"), InlineKeyboardButton(text="✏️ Изменить Содержание", callback_data="pub_user_change_body"))
    builder.row(InlineKeyboardButton(text="✏️ Изменить Изображение", callback_data="pub_user_change_img"), InlineKeyboardButton(text=f"Тип: {type}", callback_data="pub_user_change_type"))
    builder.row(InlineKeyboardButton(text="✅ Предложить", callback_data="pub_user_change_publish"), InlineKeyboardButton(text="⬅️ Отмена", callback_data="go_to_profile"))
    await callback.bot.send_photo(callback.message.chat.id, photo=FSInputFile(f"assets/photos/requests_photos/{user_redact[2]}"), caption=f"<b>{user_redact[0]}</b>\n{user_redact[1]}", reply_markup=builder.as_markup())
    await callback.answer()


async  def go_to_redact_user_publish_from_message(message: Message):
    user_redact = User_publish_redact[message.from_user.id]
    builder = InlineKeyboardBuilder()
    type = {"fact":"факт", "place":"место"}[User_publish_redact[message.from_user.id][3]]
    builder.row(InlineKeyboardButton(text="✏️ Изменить Название", callback_data="pub_user_change_name"),
                InlineKeyboardButton(text="✏️ Изменить Содержание", callback_data="pub_user_change_body"))
    builder.row(InlineKeyboardButton(text="✏️ Изменить Изображение", callback_data="pub_user_change_img"),
                InlineKeyboardButton(text=f"Тип: {type}", callback_data="pub_user_change_type"))
    builder.row(InlineKeyboardButton(text="✅ Предложить", callback_data="pub_user_change_publish"),
                InlineKeyboardButton(text="⬅️ Отмена", callback_data="go_to_profile"))
    await message.bot.send_photo(message.chat.id, photo=FSInputFile(f"assets/photos/requests_photos/{user_redact[2]}"), caption=f"<b>{user_redact[0]}</b>\n{user_redact[1]}", reply_markup=builder.as_markup())


async def go_to_tasks(callback: CallbackQuery):
    builder = InlineKeyboardBuilder()
    tasks = CUR.execute("SELECT * FROM tasks").fetchall()
    balance = CUR.execute(f"SELECT balance FROM users WHERE telegram_id={callback.from_user.id}").fetchall()[0][0]
    for task in tasks:
        users = task[2].split(";")
        if str(callback.from_user.id) not in users:
            builder.row(InlineKeyboardButton(text=f"{task[1]}: {task[3]}🪙", callback_data=f"task_{task[0]}"))
    builder.row(InlineKeyboardButton(text="⬅️ Назад", callback_data="go_to_market"))
    await callback.message.answer(f"Ваш баланс: {balance}\nВыберите доступное задание:", reply_markup=builder.as_markup())
    await callback.answer()

async def go_to_offers(callback: CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Промокод на онлайн-заказ в ЧитайГород: 1000🪙", callback_data="offer_promocode"))
    builder.row(InlineKeyboardButton(text="⬅️ Назад", callback_data="go_to_market"))
    balance = CUR.execute(f"SELECT balance FROM users WHERE telegram_id={callback.from_user.id}").fetchall()[0][0]
    await callback.message.answer(f"Добро пожаловать в оффер-маркет, сдесь вы можете приобрести промокоды на покупку сувениров, особого статуса и т. д.\nВаш баланс: {balance}", reply_markup=builder.as_markup())
    await callback.answer()



functions = {
    "go_to_home":go_to_home,
    "go_to_storage":go_to_storage,
    "go_to_profile":go_to_profile,
    "go_to_market":go_to_market,
    "go_to_facts":go_to_facts,
    "go_to_random_fact":go_to_random_fact,
    "go_to_places":go_to_places,
    "go_to_random_place":go_to_random_place,
    "go_to_requests":go_to_requests,
    "go_to_make_request":go_to_make_request,
    "go_to_redact_user_publish":go_to_redact_user_publish,
    "go_to_tasks":go_to_tasks,
    "go_to_offers":go_to_offers
}
