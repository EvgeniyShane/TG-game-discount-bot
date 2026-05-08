from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from db.users import get_user, users
from utils.reply import reply


async def settings_menu(update, context):
    user = get_user(update.effective_user.id)

    settings = user.get("settings", {}) if user else {}
    min_discount = settings.get("min_discount", 20)
    notifications = settings.get("notifications", True)

    status = "ВКЛ 🔔" if notifications else "ВЫКЛ 🔕"

    keyboard = [
        [
            InlineKeyboardButton("➖ 10", callback_data="disc_-10"),
            InlineKeyboardButton("➕ 10", callback_data="disc_+10"),
        ],
        [
            InlineKeyboardButton("🔔 Вкл/Выкл", callback_data="toggle_notify")
        ]
    ]

    text = (
        "⚙️ <b>Настройки</b>\n\n"
        f"📉 Мин. скидка: <b>{min_discount}%</b>\n"
        f"🔔 Уведомления: <b>{status}</b>"
    )

    await reply(update, text, InlineKeyboardMarkup(keyboard))
    
async def change_discount(update, context, delta):
    user_id = update.effective_user.id
    user = get_user(user_id)

    current = user.get("settings", {}).get("min_discount", 20)
    new_value = max(0, min(100, current + delta))

    users.update_one(
        {"telegram_id": user_id},
        {"$set": {"settings.min_discount": new_value}}
    )

    await settings_menu(update, context)


async def toggle_notifications(update, context):
    user_id = update.effective_user.id
    user = get_user(user_id)

    current = user.get("settings", {}).get("notifications", True)
    new_value = not current

    users.update_one(
        {"telegram_id": user_id},
        {"$set": {"settings.notifications": new_value}}
    )

    await settings_menu(update, context)