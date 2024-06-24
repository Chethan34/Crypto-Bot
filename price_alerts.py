from db import Database
from api import AlphaVantageGraphQLWrapper

db = Database()
api = AlphaVantageGraphQLWrapper()

async def check_price_alerts(context):
    alerts = db.get_alerts()
    for alert in alerts:
        current_price = api.get_stock_price(alert['symbol'])['price']
        if alert['alert_type'] == 'entry' and current_price <= alert['price']:
            await context.bot.send_message(chat_id=alert['user_id'], 
                                           text=f"Entry point alert: {alert['symbol']} has reached ₹{current_price}")
            db.remove_alert(alert['_id'])
        elif alert['alert_type'] == 'profit' and current_price >= alert['price']:
            await context.bot.send_message(chat_id=alert['user_id'], 
                                           text=f"Profit level alert: {alert['symbol']} has reached ₹{current_price}")
            db.remove_alert(alert['_id'])
        elif alert['alert_type'] == 'loss' and current_price <= alert['price']:
            await context.bot.send_message(chat_id=alert['user_id'], 
                                           text=f"Stop loss alert: {alert['symbol']} has reached ₹{current_price}")
            db.remove_alert(alert['_id'])