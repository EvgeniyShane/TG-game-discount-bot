from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from db.users import get_user, users
from services.steam import search_games, get_game
from utils.reply import reply


async def add_game(update, context):
    context.user_data["state"] = "waiting_game"
    await reply(update, "Название игры?")


# 🔥 ОБНОВИЛИ
async def list_games(update, context):
    user = get_user(update.effective_user.id)

    if not user or not user.get("wishlist"):
        return await reply(update, "Пусто")

    keyboard = []
    text = "🎮 <b>Твои игры:</b>\n\n"

    for g in user["wishlist"]:
        title = g["title"]
        text += f"• {title}\n"

        keyboard.append([
            InlineKeyboardButton(
                f"❌ {title[:25]}",
                callback_data=f"del_{g['game_id']}"
            )
        ])

    await reply(update, text, InlineKeyboardMarkup(keyboard))


async def handle_game_select(update, context, text):
    games = await search_games(text)

    if not games:
        return await reply(update, "Не найдено")

    keyboard = [
        [InlineKeyboardButton(
            g.get("external", "Unknown"),
            callback_data=f"add_{g['gameID']}"
        )]
        for g in games
    ]

    await reply(update, "Выбор:", InlineKeyboardMarkup(keyboard))


async def add_to_wishlist(update, context, game_id):
    game = await get_game(game_id)

    if not game:
        return await reply(update, "Ошибка 😢")

    title = game["info"].get("title", "Unknown")

    users.update_one(
        {"telegram_id": update.effective_user.id},
        {
            "$addToSet": {
                "wishlist": {
                    "game_id": game_id,
                    "title": title,
                    "last_discount": 0
                }
            }
        },
        upsert=True
    )

    await reply(update, f"✅ Добавлено: {title}")



async def remove_from_wishlist(update, context, game_id):
    user_id = update.effective_user.id

    users.update_one(
        {"telegram_id": user_id},
        {
            "$pull": {
                "wishlist": {"game_id": game_id}
            }
        }
    )

    await reply(update, "❌ Игра удалена")