import asyncio
import os
import sys
import time
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# Hardcoded fallback credentials to guarantee deployment
API_ID = int(os.getenv("API_ID", "32617470"))
API_HASH = os.getenv("API_HASH", "19b2c75634d9ebcd7078b3ce54dbfe50").strip()

DEFAULT_SESSION = "1BJWap1sBu4dekJcrc7RYu3cDFvakOqF3kEgCXpnlb2hHpvZmCxPYsqWZYURKMozT8cbyxI2xqzYPC-09naIt93SLcLPZl7M5FsuZzuNU3hBdrehqkn6zie4kmKAlChNAMFnS4CLfbpmN1oundpz2Qf-BqyvL_pXUPRviQlVOrJ4FOzoWWTz5PfNdRo_zee7vIvCM1mrwkP35unb2v1WVALGwXxQlR9DVvn4BG-mmhL-MdjXuxdsRflo0oCqWPRGiTHHY2br4bVXoRlXXE_EX6XxVqferMsJdjz3fSrD9d22ztfzJN5BN0T-1flAnAUcn-id1M4mnqGZ0Pa8dDRWCFr8a80QUBRg="

# Fetch environment variable or fallback to default
raw_session = os.getenv("STRING_SESSION") or DEFAULT_SESSION
SESSION_STRING = raw_session.strip().strip('"').strip("'")

# Auto-reply text with payment details and links
REPLY_TEXT = """🔮 <b>✦ GUSE CAR EKUB ✦</b> 🔮

👇👇👇👇👇👇👇👇👇👇

<a href="https://t.me/mameekub_bot"><b>ENTER BOT</b></a>

<a href="https://t.me/gusecarekub1"><b>JOIN GROUP</b></a>

👆👆👆👆👆👆👆👆👆👆

💳 <b>Payment Details:</b>
CBE > <code>1000777754142</code>
Bontu kebeda & Tesfaye Daba
Telebirr: <code>0922192323</code>"""

client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

# Tracks user_id -> timestamp (in seconds) of last auto-reply sent
user_last_replied = {}
TWENTY_FOUR_HOURS = 86400  # 24 hours in seconds


@client.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def auto_reply(event):
    sender = await event.get_sender()
    if not sender or getattr(sender, "bot", False):
        return

    user_id = sender.id
    current_time = time.time()

    # Check if we replied to this user in the last 24 hours
    if user_id in user_last_replied:
        elapsed = current_time - user_last_replied[user_id]
        if elapsed < TWENTY_FOUR_HOURS:
            return  # Skip reply if 24 hours haven't passed yet

    # Update or set the last replied timestamp for this user
    user_last_replied[user_id] = current_time
    await asyncio.sleep(1)

    await event.reply(
        message=REPLY_TEXT,
        parse_mode="html",
        link_preview=False,
    )


async def main():
    print("Starting autoresponder worker with 24h interval rate-limiter...")
    await client.connect()

    if not await client.is_user_authorized():
        print(
            "\n❌ CRITICAL ERROR: Session string is invalid or expired! Generate a new session string."
        )
        sys.exit(1)

    print("Account is successfully online and monitoring private messages!")
    await client.run_until_disconnected()


if __name__ == "__main__":
    asyncio.run(main())
