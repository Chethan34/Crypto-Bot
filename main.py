import logging
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from dotenv import load_dotenv
import os
from handlers.start import start
from handlers.price import price
from handlers.alert import set_alert, check_alerts
from handlers.chart import chart
from handlers.historical import historical
from handlers.global_data import global_command, button_callback

# Load environment variables
load_dotenv()

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    # Create the Updater and pass it your bot's token
    updater = Updater(os.getenv('TELEGRAM_BOT_TOKEN'), use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Register command handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("price", price))
    dp.add_handler(CommandHandler("alert", set_alert))
    dp.add_handler(CommandHandler("chart", chart))
    dp.add_handler(CommandHandler("historical", historical))
    dp.add_handler(CommandHandler("global", global_command))


    # Register callback query handlers
    dp.add_handler(CallbackQueryHandler(button_callback, pattern='^(?!nft).*$'))

    # Set up job queue for checking alerts
    job_queue = updater.job_queue
    job_queue.run_repeating(check_alerts, interval=300, first=0)  # Run every 5 minutes

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT, SIGTERM or SIGABRT
    updater.idle()

if __name__ == "__main__":
    main()
