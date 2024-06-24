from pymongo import MongoClient
from config import MONGODB_URI

client = MongoClient(MONGODB_URI)
db = client['stock_bot']
alerts_collection = db['alerts']

def init_db():
    alerts_collection.create_index([('user_id', 1), ('stock_name', 1)])

def insert_alert(alert_data):
    alerts_collection.insert_one(alert_data)

def get_alerts():
    return list(alerts_collection.find())

def remove_alert(alert_id):
    alerts_collection.delete_one({'_id': alert_id})

#todo - git add . database