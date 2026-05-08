from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from utils.reply import reply


async def menu(update, context):
    keyboard = [
        [InlineKeyboardButton("👤 Профиль", callback_data="profile")],
        [InlineKeyboardButton("💰 Баланс", callback_data="balance")],
        [InlineKeyboardButton("🎮 Мои игры", callback_data="list_games")],
        [InlineKeyboardButton("➕ Добавить игру", callback_data="add_game")],
        [InlineKeyboardButton("🎰 Рулетка", callback_data="slots")],
        [InlineKeyboardButton("📊 Статистика", callback_data="stats")],
        [InlineKeyboardButton("⚙️ Настройки", callback_data="settings")],
        [InlineKeyboardButton("ℹ️ Помощь", callback_data="help")]
    ]

    await reply(
        update,
        "📋 <b>Главное меню</b>\nВыбери действие:",
        InlineKeyboardMarkup(keyboard)
    )