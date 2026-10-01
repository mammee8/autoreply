import asyncio
import os
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# Account Credentials (from Environment Variables)
API_ID = int(os.getenv("API_ID", "32617470"))
API_HASH = os.getenv("API_HASH", "19b2c75634d9ebcd7078b3ce54dbfe50")
SESSION_STRING = os.getenv("1BJWap1sBu0jth4bb5A8dy7iQyEgDRL_R2DXL3uk0_XIU_2OaOrEZneahG4Tf9E2AFcYD6oQZSEANr2A2xtmP0jEw3Kc19cyNtlC27ipJqP8XcTm0UBpknjy5N50-focdCCuEXjiIJLfgfsMc7ryaQ92RVYe1Lu4NhIyPAuA7Qe_cD-8rC1gQsPvKj_GMwkgkj9AeLSKRpYq-CFLAhGTFtthzq6TuxT1UjXcO1nhnENkdFlsGtI1Uc1wi6_wjV9-rfW2_yfYsehNaAROOI1BSpPRnueYfKIcGZ4I3JX6twiaVE9UEqVSPqyCCrtpmwo-Da3cxNBhlgvSwjfVuFs1H45L-R8DRsNQ=")

# Auto-reply message content
REPLY_TEXT = """🔮 <b>✦ GUSE CAR EKUB ✦</b> 🔮

👇👇👇👇👇👇👇👇👇👇

<a href="https://t.me/mameekub_bot"><b>ENTER BOT</b></a>

<a href="https://t.me/gusecarekub1"><b>JOIN GROUP</b></a>

👆👆👆👆👆👆👆👆👆👆"""

# Initialize single client using StringSession
client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

replied_users = set()

@client.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def auto_reply(event):
    sender = await event.get_sender()
    if not sender or getattr(sender, "bot", False):
        return

    user_id = sender.id
    if user_id in replied_users:
        return

    replied_users.add(user_id)
    await asyncio.sleep(1)

    await event.reply(
        message=REPLY_TEXT,
        parse_mode="html",
        link_preview=False,
    )

async def main():
    print("Starting single-account autoresponder...")
    await client.start()
    print("Account is online!")
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
