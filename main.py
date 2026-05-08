from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters
)

from config import TOKEN
from jobs.discount_job import discount_loop
import asyncio

from handlers.start import start
from handlers.callback import callback_handler
from handlers.games import add_game
from handlers.menu import menu
from handlers.text import handle_text
from handlers.profile import profile
from handlers.balance import balance
from handlers.stats import stats
from handlers.profile_edit import setname
from handlers.help import help_command


app = ApplicationBuilder().token(TOKEN).build()

async def post_init(app):
    app.discount_task = asyncio.create_task(discount_loop(app))


app.post_init = post_init


app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("menu", menu))
app.add_handler(CommandHandler("add", add_game))
app.add_handler(CommandHandler("profile", profile))
app.add_handler(CommandHandler("balance", balance))
app.add_handler(CommandHandler("stats", stats))
app.add_handler(CommandHandler("setname", setname))
app.add_handler(CommandHandler("help", help_command))

app.add_handler(CallbackQueryHandler(callback_handler))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))


print("BOT RUNNING")
app.run_polling()