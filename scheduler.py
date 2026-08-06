import asyncio

from alerts import get_hot_tokens


async def run_scheduler(bot):

    print("✅ Alert Engine pornit!")

    while True:

        tokens = get_hot_tokens()

        if len(tokens) > 0:

            print(f"Au fost găsite {len(tokens)} tokenuri noi.")

        await asyncio.sleep(60)