import asyncio
import os
import sys
import time

from telethon import TelegramClient, events
from telethon.sessions import StringSession


# ============================================================
# TELEGRAM CONFIGURATION
# ============================================================

try:
    API_ID = int(os.environ["API_ID"])
except (KeyError, ValueError):
    print("❌ ERROR: API_ID is missing or invalid.")
    sys.exit(1)

API_HASH = os.environ.get("API_HASH", "").strip()
STRING_SESSION = os.environ.get("STRING_SESSION", "").strip()

if not API_HASH:
    print("❌ ERROR: API_HASH environment variable is missing.")
    sys.exit(1)

if not STRING_SESSION:
    print("❌ ERROR: STRING_SESSION environment variable is missing.")
    sys.exit(1)

# Remove accidental quotes if Render variable was entered as:
# "session_string"
STRING_SESSION = STRING_SESSION.strip('"').strip("'")


# ============================================================
# AUTO-REPLY MESSAGE
# ============================================================

REPLY_TEXT = """🔮 <b>✦ GUSE CAR EKUB ✦</b> 🔮

👇👇👇👇👇👇👇👇👇👇

<a href="https://t.me/mameekub_bot"><b>ENTER BOT</b></a>

<a href="https://t.me/gusecarekub1"><b>JOIN GROUP</b></a>

👆👆👆👆👆👆👆👆👆👆

💳 <b>Payment Details:</b>
CBE &gt; <code>1000777754142</code>
Bontu kebeda &amp; Tesfaye Daba
Telebirr: <code>0922192323</code>
"""


# ============================================================
# TELEGRAM CLIENT
# ============================================================

client = TelegramClient(
    StringSession(STRING_SESSION),
    API_ID,
    API_HASH,
)


# ============================================================
# RATE LIMIT
# ============================================================

# user_id -> timestamp of last reply
user_last_replied = {}

TWENTY_FOUR_HOURS = 24 * 60 * 60


# ============================================================
# AUTO REPLY HANDLER
# ============================================================

@client.on(
    events.NewMessage(
        incoming=True,
        func=lambda event: event.is_private
    )
)
async def auto_reply(event):

    try:
        sender = await event.get_sender()

        # Ignore users that cannot be identified
        if not sender:
            return

        # Ignore bots
        if getattr(sender, "bot", False):
            return

        user_id = sender.id
        current_time = time.time()

        # Check whether we already replied within 24 hours
        last_reply = user_last_replied.get(user_id)

        if last_reply is not None:
            elapsed = current_time - last_reply

            if elapsed < TWENTY_FOUR_HOURS:
                return

        # Save reply timestamp
        user_last_replied[user_id] = current_time

        # Small delay
        await asyncio.sleep(1)

        # Send reply
        await event.reply(
            message=REPLY_TEXT,
            parse_mode="html",
            link_preview=False,
        )

        print(f"✅ Auto-replied to user {user_id}")

    except Exception as error:
        print(f"❌ Error while replying: {error}")


# ============================================================
# MAIN
# ============================================================

async def main():

    print("========================================")
    print("🚀 Starting Telegram autoresponder")
    print("========================================")

    print("🔌 Connecting to Telegram...")

    try:
        await client.connect()

    except Exception as error:
        print(f"❌ Telegram connection failed: {error}")
        sys.exit(1)

    # --------------------------------------------------------
    # Check authentication
    # --------------------------------------------------------

    try:
        authorized = await client.is_user_authorized()

    except Exception as error:
        print(f"❌ Failed to check Telegram authorization: {error}")
        await client.disconnect()
        sys.exit(1)

    if not authorized:

        print("")
        print("========================================")
        print("❌ TELEGRAM SESSION INVALID")
        print("========================================")
        print("")
        print("Your STRING_SESSION is invalid, expired,")
        print("revoked, or was generated with different")
        print("API_ID/API_HASH credentials.")
        print("")
        print("Generate a NEW Telethon StringSession and")
        print("replace STRING_SESSION in Render.")
        print("")
        print("========================================")

        await client.disconnect()
        sys.exit(1)

    # --------------------------------------------------------
    # Successfully authenticated
    # --------------------------------------------------------

    me = await client.get_me()

    print("")
    print("========================================")
    print("✅ TELEGRAM ACCOUNT CONNECTED")
    print("========================================")

    if me:
        print(f"👤 Name: {me.first_name or ''}")
        print(f"🆔 User ID: {me.id}")
        print(f"📱 Username: @{me.username}" if me.username else "📱 Username: None")

    print("")
    print("🤖 Autoresponder is running")
    print("⏱️ Reply interval: 24 hours per user")
    print("========================================")
    print("")

    # Keep the application running
    await client.run_until_disconnected()


# ============================================================
# START APPLICATION
# ============================================================

if __name__ == "__main__":
    try:
        asyncio.run(main())

    except KeyboardInterrupt:
        print("\n🛑 Application stopped.")

    except Exception as error:
        print(f"\n❌ CRITICAL ERROR: {error}")
        sys.exit(1)