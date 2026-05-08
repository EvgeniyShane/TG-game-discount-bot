from db.mongo import users
from utils.reply import reply
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


async def stats(update, context):
    # пока заглушка
    text = (
        "📊 <b>Статистика</b>\n\n"
        "Скоро здесь будет больше данных 👀"
    )

    keyboard = [
        [InlineKeyboardButton("⬅️ Меню", callback_data="menu")]
    ]

    await reply(update, text, InlineKeyboardMarkup(keyboard))