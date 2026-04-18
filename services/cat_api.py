import aiohttp
from config import CAT_API_LIMIT_MAX, CAT_API_TIMEOUT

async def fetch_cat_urls(count: int) -> list[str]:
    count = max(1, min(count, CAT_API_LIMIT_MAX))
    url = "https://api.thecatapi.com/v1/images/search"

    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(CAT_API_TIMEOUT)) as session:
        async with session.get(url, params = {"limit": count}) as response:
            if response.status != 200:
                return []
            data = await response.json()
            return [cat["url"] for cat in data][:count]

async def download_image_bytes(session: aiohttp.ClientSession, url: str) -> bytes | None:
    try:
        async with session.get(url) as resp:
            return await resp.read() if resp.status == 200 else None
    except Exception:
        return None