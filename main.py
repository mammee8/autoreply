import asyncio
import os
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# Account 1 Credentials
API_ID_1 = int(os.getenv("API_ID_1", "36389627"))
API_HASH_1 = os.getenv("API_HASH_1", "6f8dfeee1b5a7005214c1e7a71b40455")
SESSION_1 = os.getenv("STRING_SESSION_1")

# Account 2 Credentials
API_ID_2 = int(os.getenv("API_ID_2"))
API_HASH_2 = os.getenv("API_HASH_2")
SESSION_2 = os.getenv("STRING_SESSION_2")

REPLY_TEXT = """🔮 <b>✦ GUSE CAR EKUB ✦</b> 🔮

👇👇👇👇👇👇👇👇👇👇

<a href="https://t.me/Gusecar2bot"><b>ENTER BOT</b></a>

<a href="https://t.me/gusecarekub1"><b>JOIN GROUP</b></a>

👆👆👆👆👆👆👆👆👆👆"""

# Clients initialized via StringSession
client1 = TelegramClient(StringSession(SESSION_1), API_ID_1, API_HASH_1)
client2 = TelegramClient(StringSession(SESSION_2), API_ID_2, API_HASH_2)

replied_users_1 = set()
replied_users_2 = set()

@client1.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def auto_reply_1(event):
    sender = await event.get_sender()
    if not sender or getattr(sender, "bot", False):
        return
    if sender.id in replied_users_1:
        return
    replied_users_1.add(sender.id)
    await asyncio.sleep(1)
    await event.reply(message=REPLY_TEXT, parse_mode="html", link_preview=False)

@client2.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def auto_reply_2(event):
    sender = await event.get_sender()
    if not sender or getattr(sender, "bot", False):
        return
    if sender.id in replied_users_2:
        return
    replied_users_2.add(sender.id)
    await asyncio.sleep(1)
    await event.reply(message=REPLY_TEXT, parse_mode="html", link_preview=False)

async def main():
    print("Starting background workers...")
    await client1.start()
    await client2.start()
    print("Both accounts online!")
    await asyncio.gather(
        client1.run_until_disconnected(),
        client2.run_until_disconnected()
    )

if __name__ == "__main__":
    asyncio.run(main())
