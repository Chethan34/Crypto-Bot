from telegram import Update
from telegram.ext import CallbackContext

def start(update: Update, context: CallbackContext) -> None:
    welcome_message = (
        "👋 Welcome to the Crypto Bot! 🚀\n\n"
        "*Available Commands:*\n"
        "💰 /price <coin> - Show today's price\n"
        "📈 /chart <coin> - Last 7 days chart\n"
        "📊 /historical <coin> - Past 7 days price data\n"
        "📦 /txhash <hash> - Details of a transaction\n"
        "=======================================\n"
        "💡 *Examples:*\n"
        "`/price bitcoin`\n"
        "`/chart eth`\n"
        "`/historical solana`\n"
        "`/txhash 0x123...`\n"
    )
    update.message.reply_text(welcome_message, parse_mode="Markdown")
