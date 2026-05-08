from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from utils.reply import reply


async def help_command(update, context):
    keyboard = [
        [InlineKeyboardButton("📋 Открыть меню", callback_data="menu")]
    ]

    await reply(
        update,
        "🤖 <b>Помощь по боту</b>\n\n"
        "🎮 Я бот для отслеживания скидок на игры и мини-игр.\n\n"
        "📌 <b>Основные команды:</b>\n"
        "/menu — открыть меню\n"
        "/profile — твой профиль\n"
        "/balance — баланс\n"
        "/add — добавить игру в список\n"
        "/list — твои игры\n"
        "/slots — мини-игра\n"
        "/earn — получить монеты\n\n"
        "💡 <b>Совет:</b> используй меню — так быстрее 😉",
        InlineKeyboardMarkup(keyboard)
    )
