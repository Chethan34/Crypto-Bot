import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from config import TOKEN

# Logging configuration
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Command handlers
def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to the Stock Bot! Use /help to see available commands.")

def help_command(update: Update, context: CallbackContext):
    help_text = """
    Available commands:
    /price ₹[name] - Get current stock price
    /intra ₹[name] - Get intraday chart
    /chart ₹[name] - Get monthly chart
    /alerts [name] [price] [type] - Set price alert
    """
    context.bot.send_message(chat_id=update.effective_chat.id, text=help_text)

# Start Bot
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))

    
    updater.start_polling()
    logger.info("Stock Bot started polling...")
    updater.idle()
#Entry
if __name__ == '__main__':
    main()
