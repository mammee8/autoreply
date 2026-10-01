import asyncio
import os
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# Account Credentials (from Environment Variables)
API_ID = int(os.getenv("API_ID", "36389627"))
API_HASH = os.getenv("API_HASH", "6f8dfeee1b5a7005214c1e7a71b40455")
SESSION_STRING = os.getenv("STRING_SESSION")

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
