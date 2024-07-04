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
        "/historical <coin> <days> - Get historical price data\n"
        "/global - View global cryptocurrency market data\n"
        "/nfts - View top traded NFTs and trade count chart\n\n"
        "Example usage:\n"
        "/price bitcoin\n"
        "/alert ethereum 2000\n"
        "/chart dogecoin\n"
        "/historical cardano 30\n"
        "/global\n"
    )
    update.message.reply_text(welcome_message)