from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from config import ALPHA_VANTAGE_API_KEY

# Fetching data 
transport = RequestsHTTPTransport(url=f'https://www.alphavantage.co/query?apikey={"CVOT9HBT60FB5W7I"}')
client = Client(transport=transport, fetch_schema_from_transport=True)

def get_stock_price(stock_name):
    query = gql('''
    query GetStockPrice(₹symbol: String!) {
        globalQuote(symbol: ₹symbol) {
            symbol
            price
            change
            changePercent
        }
    }
    ''')