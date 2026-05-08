import logging
from collections import defaultdict

from db.users import users
from services.steam import get_game


async def check_discounts(bot):
    all_users = list(users.find())

    game_to_users = defaultdict(list)

    # собираем: игра → пользователи
    for user in all_users:
        for game in user.get("wishlist", []):
            game_id = game.get("game_id")
            if not game_id:
                continue
            game_to_users[game_id].append(user)

    # проверяем каждую игру
    for game_id, user_list in game_to_users.items():
        try:
            data = await get_game(game_id)

            if not data:
                continue

            deals = data.get("deals", [])
            if not deals:
                continue

            deal = deals[0]

            # защита от кривых данных
            try:
                price = float(deal["price"])
                normal = float(deal["retailPrice"])
            except (KeyError, ValueError, TypeError):
                continue

            if normal == 0:
                continue

            discount = int((1 - price / normal) * 100)

            if discount <= 0:
                continue

            title = data.get("info", {}).get("title", "Unknown")

            logging.info(f"[CHECK] {title} → {discount}%")

            for user in user_list:
                user_id = user.get("telegram_id")
                if not user_id:
                    continue

                username = user.get("username", "unknown")
                wishlist = user.get("wishlist", [])

                g = next(
                    (x for x in wishlist if x.get("game_id") == game_id),
                    None
                )

                if not g:
                    continue

                last = g.get("last_discount", 0)

                if discount <= last or discount < 20:
                    continue

                sent = False

                try:
                    await bot.send_message(
                        chat_id=user_id,
                        text=(
                            f"🔥 <b>{title}</b>\n"
                            f"💰 {price}$ (-{discount}%)"
                        ),
                        parse_mode="HTML"
                    )
                    sent = True

                except Exception as e:
                    err = str(e)

                    logging.error(
                        f"Send error | user_id={user_id} | username={username} | game={title} | error={err}"
                    )

                    if any(x in err for x in ["blocked", "chat not found", "deactivated"]):
                        logging.warning(
                            f"BLOCKED | user_id={user_id} | username={username}"
                        )

                if sent:
                    users.update_one(
                        {
                            "telegram_id": user_id,
                            "wishlist.game_id": game_id
                        },
                        {
                            "$set": {
                                "wishlist.$.last_discount": discount
                            }
                        }
                    )

        except Exception as e:
            logging.error(f"Game processing error | game_id={game_id} | error={e}")