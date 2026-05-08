from db.mongo import users


def get_user(user_id: int):
    return users.find_one({"telegram_id": user_id})


def upsert_user(tg_user):
    users.update_one(
        {"telegram_id": tg_user.id},
        {
            "$set": {
                "telegram_id": tg_user.id,
                "username": tg_user.username,
                "first_name": tg_user.first_name,
                "last_name": tg_user.last_name
            },
            "$setOnInsert": {
                "balance": 100,
                "wishlist": []
            }
        },
        upsert=True
    )


def add_balance(user_id: int, amount: int):
    users.update_one(
        {"telegram_id": user_id},
        {"$inc": {"balance": amount}},
        upsert=True
    )