import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from utils.graph_api import (
    fetch_total_market_cap_chart, 
    fetch_bitcoin_dominance_chart, 
    fetch_defi_market_cap_chart,
    fetch_fear_and_greed_chart
)

logger = logging.getLogger(__name__)

def global_command(update: Update, context: CallbackContext) -> None:
    try:
        message = (
            "Global Crypto Market Data:\n\n"
            "Select a chart to view:"
        )

        keyboard = [
            [InlineKeyboardButton("Total Market Cap", callback_data='total_market_cap_chart')],
            [InlineKeyboardButton("Bitcoin Dominance", callback_data='bitcoin_dominance_chart')],
            [InlineKeyboardButton("DeFi Market Cap", callback_data='defi_market_cap_chart')],
            [InlineKeyboardButton("Fear and Greed Index", callback_data='fear_and_greed_chart')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        update.message.reply_text(message, reply_markup=reply_markup)
    except Exception as e:
        logger.error(f"Error in global_command: {str(e)}")
        update.message.reply_text("An error occurred while fetching global data. Please try again later.")

def button_callback(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    try:
        if query.data == 'total_market_cap_chart':
            chart_buf = fetch_total_market_cap_chart()
            caption = "Total Market Cap over the last year."
        elif query.data == 'bitcoin_dominance_chart':
            chart_buf = fetch_bitcoin_dominance_chart()
            caption = "Bitcoin Dominance over the last year."
        elif query.data == 'defi_market_cap_chart':
            chart_buf = fetch_defi_market_cap_chart()
            caption = "DeFi Market Cap over the last year."
        elif query.data == 'fear_and_greed_chart':
            chart_buf = fetch_fear_and_greed_chart()
            caption = "Fear and Greed Index over the last year."
        else:
            chart_buf = None
            caption = "Unknown chart type."

        if chart_buf:
            query.message.reply_photo(photo=chart_buf, caption=caption)
        else:
            query.message.reply_text("Sorry, there was an error generating the chart. Please try again later.")

    except Exception as e:
        logger.error(f"Error in button_callback: {str(e)}")
        query.message.reply_text("An error occurred while processing your request. Please try again later.")