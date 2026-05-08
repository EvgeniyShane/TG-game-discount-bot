import aiohttp


async def fetch_json(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as r:
            if r.status != 200:
                return None
            return await r.json()


async def search_games(title: str):
    data = await fetch_json(
        f"https://www.cheapshark.com/api/1.0/games?title={title}"
    )

    return data[:5] if isinstance(data, list) else []


async def get_game(game_id: str):
    data = await fetch_json(
        f"https://www.cheapshark.com/api/1.0/games?id={game_id}"
    )

    if isinstance(data, dict) and "info" in data:
        return data

    return None