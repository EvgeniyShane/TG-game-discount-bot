import logging

from handlers.menu import menu
from handlers.profile import profile
from handlers.balance import balance
from handlers.stats import stats
from handlers.games import add_game, list_games, add_to_wishlist, remove_from_wishlist
from handlers.help import help_command
from handlers.slots import slots
from handlers.settings import settings_menu, change_discount, toggle_notifications
from utils.reply import reply


async def callback_handler(update, context):
    q = update.callback_query

    if not q or not q.data:
        return

    await q.answer()
    data = q.data

    try:
        if data == "profile":
            await profile(update, context)

        elif data == "menu":
            await menu(update, context)

        elif data == "balance":
            await balance(update, context)

        elif data == "stats":
            await stats(update, context)

        elif data == "add_game":
            await add_game(update, context)

        elif data == "list_games":
            await list_games(update, context)

        elif data == "setname":
            context.user_data["state"] = "waiting_name"
            await reply(update, "✏️ Введи новое имя:")

        elif data == "help":
            await help_command(update, context)

        elif data == "slots":
            await slots(update, context)

        elif data == "settings":
            await settings_menu(update, context)

        
        elif data.startswith("add_"):
            parts = data.split("_", 1)
            if len(parts) < 2:
                return await reply(update, "Ошибка данных 😢")

            game_id = parts[1]
            await add_to_wishlist(update, context, game_id)

     
        elif data.startswith("del_"):
            parts = data.split("_", 1)
            if len(parts) < 2:
                return await reply(update, "Ошибка удаления 😢")

            game_id = parts[1]
            await remove_from_wishlist(update, context, game_id)
            await list_games(update, context)

        
        elif data.startswith("disc_"):
            parts = data.split("_", 1)
            if len(parts) < 2:
                return await reply(update, "Ошибка 😢")

            value = int(parts[1])
            await change_discount(update, context, value)

       
        elif data == "toggle_notify":
            await toggle_notifications(update, context)

        else:
            await reply(update, "Неизвестное действие 🤔")

    except Exception as e:
        logging.error(f"Callback error: {e}")
        await reply(update, "Произошла ошибка 😢")