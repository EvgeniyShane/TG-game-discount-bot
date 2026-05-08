import random
from db.users import get_user, users
from utils.reply import reply


async def slots(update, context):
    user_id = update.effective_user.id
    data = get_user(user_id)

    bal = (data or {}).get("balance", 0)

    if bal < 10:
        return await reply(update, "❌ Нужно минимум 10 💰")

    users.update_one(
        {"telegram_id": user_id},
        {"$inc": {"balance": -10}}
    )

    symbols = ["🍒", "🍋", "⭐", "💎"]
    result = [random.choice(symbols) for _ in range(3)]

    win = 50 if result[0] == result[1] == result[2] else 0

    if win:
        users.update_one(
            {"telegram_id": user_id},
            {"$inc": {"balance": win}}
        )

    new_data = get_user(user_id)
    new_bal = (new_data or {}).get("balance", 0)

    if win:
        text = f"{' | '.join(result)}\n🎉 Выигрыш: {win} 💰\n💰 Баланс: {new_bal}"
    else:
        text = f"{' | '.join(result)}\n😢 Не повезло\n💰 Баланс: {new_bal}"

    await reply(update, text)