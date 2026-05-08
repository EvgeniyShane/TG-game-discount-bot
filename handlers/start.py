from db.users import upsert_user
from utils.reply import reply

from handlers.menu import menu

async def start(update, context):
    await menu(update, context)