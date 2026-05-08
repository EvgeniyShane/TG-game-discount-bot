import random
from utils.reply import reply

GREETINGS = ["привет", "здарова", "хай", "hello", "hi", "ку"]


async def handle_text(update, context):
    if not update.message or not update.message.text:
        return

    text = update.message.text
    state = context.user_data.get("state")


    if state == "waiting_game":
        context.user_data["state"] = None
        from handlers.games import handle_game_select
        return await handle_game_select(update, context, text)

    if state == "waiting_name":
        from db.users import users

        users.update_one(
            {"telegram_id": update.effective_user.id},
            {"$set": {"first_name": text}}
        )

        context.user_data["state"] = None

        return await reply(update, f"✅ Имя обновлено: {text}")

    lower_text = text.lower()
    if any(g in lower_text for g in GREETINGS):
        return await reply(update, random.choice([
            "Привет 👋",
            "Здарова 😎",
            "Хай!",
            "Hello!"
        ]))

    await reply(update, "🤔 Используй меню")