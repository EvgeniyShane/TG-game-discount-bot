import asyncio
import logging
from services.tracker import check_discounts


async def discount_loop(app):
    try:
        while True:
            try:
                print("Checking discounts...")
                await check_discounts(app.bot)
            except Exception as e:
                logging.error(f"Discount error: {e}")

            await asyncio.sleep(1800)

    except asyncio.CancelledError:
        print("Discount loop stopped")