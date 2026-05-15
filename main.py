from config import API_TOKEN

import json
import os
import telebot

bot = telebot.TeleBot(token=API_TOKEN)

ALLOWED_USERS_FILE = "allowed_users.json"

# Access does not require /start. Bots will DM results to the requester in group chats.
ACTIVATION_FILE_REQUIRED = False




def _load_allowed_user_ids() -> set[int]:
    if not os.path.exists(ALLOWED_USERS_FILE):
        return set()
    try:
        with open(ALLOWED_USERS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        ids = data.get("allowed_user_ids", []) if isinstance(data, dict) else []
        return {int(x) for x in ids}
    except Exception:
        # If file is corrupted/unreadable, fail closed.
        return set()


def _save_allowed_user_ids(user_ids: set[int]) -> None:
    data = {"allowed_user_ids": sorted(list(user_ids))}
    with open(ALLOWED_USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f)


def _can_access(message) -> bool:
    # Grant access to everyone in private after bot is activated.
    # If ACTIVATION_FILE_REQUIRED is False, treat as always activated.
    if not ACTIVATION_FILE_REQUIRED:
        return True
    return len(_load_allowed_user_ids()) > 0





def _handle_group(message, *, user_text: str, welcome_text: str) -> None:
    # For group chats: notify in group briefly, and also DM the user privately.
    name = getattr(message.from_user, "first_name", "User")

    # Short group notification (only sender will see DM; group sees this brief notice)
    bot.send_message(message.chat.id, f"@{name}, I sent you a DM.")

    # Private DM: echo user input + the actual command output.
    try:
        bot.send_message(
            message.from_user.id,
            f"You said: {user_text}\n\n{welcome_text}",
        )
    except Exception:
        # If the user hasn't started a DM chat with the bot yet, Telegram may block.
        pass







def _deny(message, text: str) -> None:
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=["start"])
def start_handler(message):
    # Allow the initiator to become the only allowed user.
    if getattr(message, "chat", None) is None or message.chat.type != "private":
        bot.send_message(message.chat.id, "Activate access by DMing me. Then send /start again in DM.")
        return


    allowed = _load_allowed_user_ids()
    allowed.add(message.from_user.id)
    _save_allowed_user_ids(allowed)
    bot.send_message(message.chat.id, "Access granted. You can now use my private commands.")


def _handle_private_command(message, welcome_text: str):
    if getattr(message, "chat", None) is None:
        return

    # In groups, DM the requester only.
    if message.chat.type != "private":
        _handle_group(message, user_text=message.text or "", welcome_text=welcome_text)
        return

    if not _can_access(message):
        _deny(message, "Access denied.")
        return

    bot.send_message(message.chat.id, welcome_text)


@bot.message_handler(commands=["explorer"])
def explorer_handler(message):
    welcome_text = (
        f"user {message.from_user.first_name} "
        "https://basescan.org/token/0x3513e4a7d27d18c2c894d98bc5a55406360b9ba3  "
    )
    _handle_private_command(message, welcome_text)


@bot.message_handler(commands=["ca"])
def ca_handler(message):
    welcome_text = (
        f"user {message.from_user.first_name} "
        "$PHAI:0x3513e4a7d27d18c2c894d98bc5a55406360b9ba3 "
    )
    _handle_private_command(message, welcome_text)


@bot.message_handler(commands=["website"])
def website_handler(message):
    welcome_text = (
        f"user {message.from_user.first_name} "
        "https://www.pharmachains.ai/ "
    )
    _handle_private_command(message, welcome_text)


@bot.message_handler(commands=["xus"])
def xus_handler(message):
    welcome_text = (
        f"user {message.from_user.first_name} "
        "https://x.com/pharmachainaius"
    )
    _handle_private_command(message, welcome_text)


@bot.message_handler(commands=["xafrica"])
def xafrica_handler(message):
    welcome_text = (
        f"user {message.from_user.first_name} "
        "https://x.com/pharmachainai"
    )
    _handle_private_command(message, welcome_text)


@bot.message_handler(commands=["instagram"])
def instagram_handler(message):
    welcome_text = (
        f"user {message.from_user.first_name} "
        "https://www.instagram.com/pharmachainai"
    )
    _handle_private_command(message, welcome_text)


@bot.message_handler(commands=["linkedin"])
def linkedin_handler(message):
    welcome_text = (
        f"user {message.from_user.first_name} "
        " https://www.linkedin.com/company/pharmachains/"
    )
    _handle_private_command(message, welcome_text)


@bot.message_handler(commands=["blog"])
def blog_handler(message):
    welcome_text = (
        f"user {message.from_user.first_name} "
        "https://pharmachains.ai/health-hub/us"
    )
    _handle_private_command(message, welcome_text)


@bot.message_handler(commands=["dexscreener"])
def dexscreener_handler(message):
    welcome_text = (
        f"user {message.from_user.first_name} "
        "https://dexscreener.com/base/0x505c61211c344E141b73057942Ce12E1E38468ee"
    )
    _handle_private_command(message, welcome_text)


if __name__ == "__main__":
    bot.polling()


