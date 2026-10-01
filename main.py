import asyncio
import os
import sys
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# Fetch credentials from Environment Variables
API_ID = int(os.getenv("API_ID", "32617470"))
API_HASH = os.getenv("API_HASH", "19b2c75634d9ebcd7078b3ce54dbfe50")
SESSION_STRING = os.getenv("1BJWap1sBu4dekJcrc7RYu3cDFvakOqF3kEgCXpnlb2hHpvZmCxPYsqWZYURKMozT8cbyxI2xqzYPC-09naIt93SLcLPZl7M5FsuZzuNU3hBdrehqkn6zie4kmKAlChNAMFnS4CLfbpmN1oundpz2Qf-BqyvL_pXUPRviQlVOrJ4FOzoWWTz5PfNdRo_zee7vIvCM1mrwkP35unb2v1WVALGwXxQlR9DVvn4BG-mmhL-MdjXuxdsRflo0oCqWPRGiTHHY2br4bVXoRlXXE_EX6XxVqferMsJdjz3fSrD9d22ztfzJN5BN0T-1flAnAUcn-id1M4mnqGZ0Pa8dDRWCFr8a80QUBRg=")

if not SESSION_STRING:
    print(
        "\n❌ CRITICAL ERROR: STRING_SESSION environment variable is missing!"
    )
    sys.exit(1)

# Auto-reply message layout
REPLY_TEXT = """🔮 <b>✦ GUSE CAR EKUB ✦</b> 🔮

👇👇👇👇👇👇👇👇👇👇

<a href="https://t.me/Gusecar2bot"><b>ENTER BOT</b></a>

<a href="https://t.me/gusecarekub1"><b>JOIN GROUP</b></a>

👆👆👆👆👆👆👆👆👆👆"""

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
    print("Starting autoresponder worker...")
    await client.connect()

    if not await client.is_user_authorized():
        print(
            "\n❌ CRITICAL ERROR: The provided STRING_SESSION is invalid or expired!"
        )
        sys.exit(1)

    print("Account is successfully online and monitoring private messages!")
    await client.run_until_disconnected()


if __name__ == "__main__":
    asyncio.run(main())
