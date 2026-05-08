from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from db.users import get_user
from utils.reply import reply


async def profile(update, context):
    user = update.effective_user
    data = get_user(user.id)

    if not data:
        return await reply(update, "Сначала нажми /start")

    name = data.get("first_name", "Не указано")
    balance = data.get("balance", 0)
    username = user.username or "—"

    text = (
        "👤 <b>Профиль</b>\n\n"
        f"ID: {user.id}\n"
        f"Имя: {name}\n"
        f"Username: @{username}\n"
        f"Баланс: {balance} 💰"
    )

    keyboard = [
        [InlineKeyboardButton("✏️ Изменить имя", callback_data="setname")],
        [InlineKeyboardButton("⬅️ Меню", callback_data="menu")]
    ]

    await reply(update, text, InlineKeyboardMarkup(keyboard))