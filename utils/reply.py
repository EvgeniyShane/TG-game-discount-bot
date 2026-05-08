async def reply(update, text, markup=None):
    msg = update.effective_message
    await msg.reply_text(text, reply_markup=markup, parse_mode="HTML")