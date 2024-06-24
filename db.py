from pymongo import MongoClient
from config import MONGODB_URI

class Database:
    def __init__(self):
        self.client = MongoClient(MONGODB_URI)
        self.db = self.client['stock_bot']
        self.users = self.db['users']
        self.alerts = self.db['alerts']

    def add_user(self, user_id):
        if not self.users.find_one({'user_id': user_id}):
            self.users.insert_one({'user_id': user_id})

    def add_alert(self, user_id, symbol, price, alert_type):
        alert = {
            'user_id': user_id,
            'symbol': symbol,
            'price': price,
            'alert_type': alert_type
        }
        self.alerts.insert_one(alert)

    def get_alerts(self):
        return list(self.alerts.find())

    def remove_alert(self, alert_id):
        self.alerts.delete_one({'_id': alert_id})