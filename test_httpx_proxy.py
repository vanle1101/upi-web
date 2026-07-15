import asyncio
import httpx

async def test():
    try:
        client = httpx.AsyncClient(proxy="http://12.34.56.78:9999", timeout=3.0)
        await client.get("https://api64.ipify.org?format=json")
        print("Success! (Uh oh, proxy was ignored!)")
    except Exception as e:
        print(f"Failed as expected: {type(e).__name__}")

asyncio.run(test())
