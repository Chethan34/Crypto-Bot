from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from config import TELEGRAM_BOT_TOKEN
from bot_commands import stock_command, intra_command, chart_command, price_alert_command, alert_callback, handle_alert_input
from price_alerts import check_price_alerts

async def start_command(update, context):
    await update.message.reply_text("Welcome to the Stock Bot! Use /help to see available commands.")

async def help_command(update, context):
    help_text = """
Available commands:
/stock ₹[name] - Get current stock price and change
/intra ₹[name] - Get intraday chart
/chart ₹[name] - Get monthly chart
/pricealert - Set price alerts
/help - Show this help message
    """
    await update.message.reply_text(help_text)

def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Add start and help commands
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))

    # Existing command handlers
    application.add_handler(CommandHandler("stock", stock_command))
    application.add_handler(CommandHandler("intra", intra_command))
    application.add_handler(CommandHandler("chart", chart_command))
    application.add_handler(CommandHandler("pricealert", price_alert_command))
    application.add_handler(CallbackQueryHandler(alert_callback))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_alert_input))

    application.job_queue.run_repeating(check_price_alerts, interval=300)

    application.run_polling()

if __name__ == '__main__':
    main()