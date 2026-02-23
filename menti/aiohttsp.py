import aiohttp
import asyncio

async def fetch_data():
    async with aiohttp.ClientSession() as session:
        async with session.get('http://127.0.0.1:8000/posts/') as response:
            data = await response.json()
            print(data)

asyncio.run(fetch_data())