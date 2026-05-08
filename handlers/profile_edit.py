from db.mongo import users
from utils.reply import reply


async def setname(update, context):
    if not context.args:
        return await reply(update, "Используй: /setname Имя")

    name = " ".join(context.args)

    users.update_one(
        {"telegram_id": update.effective_user.id},
        {"$set": {"first_name": name}},
        upsert=True
    )

    await reply(update, f"Имя обновлено: {name}")