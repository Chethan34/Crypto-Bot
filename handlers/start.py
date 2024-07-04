# handlers/start.py
from telegram import Update
from telegram.ext import CallbackContext

def start(update: Update, context: CallbackContext) -> None:
    welcome_message = (
        "Welcome to the Crypto Bot! 🚀\n\n"
        "Here are the available commands:\n"
        "/price <coin> - Get the latest price of a cryptocurrency\n"
        "/alert <coin> <price> - Set a price alert for a cryptocurrency\n"
        "/chart <coin> - Get a price chart for the last 7 days\n"
        "/historical <coin> - Get historical price data of past 7 days\n"
        "Example usage:\n"
        "/price bitcoin\n"
        "/alert ethereum 2000\n"
        "/chart dogecoin\n"
        "/historical cardano \n"
    )
    update.message.reply_text(welcome_message)