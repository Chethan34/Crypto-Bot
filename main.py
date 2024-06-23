import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from config import TOKEN

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Define command handlers
def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to the Stock Bot! Use /help to see available commands.")

def help_command(update: Update, context: CallbackContext):
    help_text = """
    Available commands:
    /price ₹[name] - Get current stock price
    /intra ₹[name] - Get intraday chart
    /chart ₹[name] - Get monthly chart
    /PriceAlert [name] [price] [type] - Set price alert
    """
    context.bot.send_message(chat_id=update.effective_chat.id, text=help_text)

# Main function to start the bot
def main():
    # Create an Updater object with the bot's token
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add command handlers to the dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))

    # Start polling for updates from Telegram
    updater.start_polling()

    # Run the bot until you press Ctrl+C
    updater.idle()

# Entry point for the script
if __name__ == '__main__':
    main()
