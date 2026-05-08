from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from db.users import get_user
from utils.reply import reply


async def balance(update, context):
    data = get_user(update.effective_user.id)
    bal = data.get("balance", 0) if data else 0

    text = (
        "💰 <b>Баланс</b>\n\n"
        f"У тебя: {bal} 💰"
    )

    keyboard = [
        [InlineKeyboardButton("⬅️ Меню", callback_data="menu")]
    ]

    await reply(update, text, InlineKeyboardMarkup(keyboard))