import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
import logging
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
import requests

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Fetch the API key from environment variables
api_key = os.getenv('BITQUERY_API_KEY')

if not api_key:
    logger.error("BITQUERY_API_KEY not found in environment variables.")
    raise ValueError("BITQUERY_API_KEY not found in environment variables.")

# Set up the GraphQL client for Bitquery
transport = RequestsHTTPTransport(
    url='https://graphql.bitquery.io',
    headers={'X-API-KEY': api_key},
    use_json=True,
)
client = Client(transport=transport, fetch_schema_from_transport=True)

def fetch_data(query, variables=None):
    try:
        return client.execute(query, variable_values=variables)
    except Exception as e:
        logger.error(f"Error fetching data: {str(e)}")
        return None

def fetch_total_market_cap():
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)

    query = gql("""
    query ($from: ISO8601DateTime, $till: ISO8601DateTime) {
      ethereum(network: ethereum) {
        dexTrades(
          options: {limit: 365, asc: "date.date"}
          date: {since: $from, till: $till}
        ) {
          date: date {
            date
          }
          tradeAmount(in: USD)
        }
      }
    }
    """)

    variables = {
        "from": start_date.isoformat(),
        "till": end_date.isoformat()
    }

    result = fetch_data(query, variables)

    if result and 'ethereum' in result and 'dexTrades' in result['ethereum']:
        trades = result['ethereum']['dexTrades']
        dates = [datetime.strptime(trade['date']['date'], '%Y-%m-%d') for trade in trades]
        values = [trade['tradeAmount'] for trade in trades]
        return dates, values
    else:
        return None, None

def fetch_bitcoin_market_cap():
    # This is a placeholder function. You'll need to implement the actual API call to get Bitcoin market cap data.
    # For now, we'll return dummy data
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    dates = [start_date + timedelta(days=i) for i in range(365)]
    values = [100000000000 + i * 1000000000 for i in range(365)]  # Dummy data
    return dates, values

def fetch_bitcoin_dominance():
    total_market_cap_dates, total_market_cap_values = fetch_total_market_cap()
    bitcoin_market_cap_dates, bitcoin_market_cap_values = fetch_bitcoin_market_cap()

    if total_market_cap_dates and bitcoin_market_cap_dates:
        dominance = [bitcoin_market_cap_values[i] / total_market_cap_values[i] * 100 for i in range(len(total_market_cap_dates))]
        return total_market_cap_dates, dominance
    
    return None, None

def fetch_defi_market_cap():
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)

    query = gql("""
    query ($from: ISO8601DateTime, $till: ISO8601DateTime) {
      ethereum(network: ethereum) {
        dexTrades(
          options: {limit: 365, asc: "date.date"}
          date: {since: $from, till: $till}
        ) {
          date: date {
            date
          }
          tradeAmount(in: USD)
        }
      }
    }
    """)

    variables = {
        "from": start_date.isoformat(),
        "till": end_date.isoformat()
    }

    result = fetch_data(query, variables)

    if result and 'ethereum' in result and 'dexTrades' in result['ethereum']:
        trades = result['ethereum']['dexTrades']
        dates = [datetime.strptime(trade['date']['date'], '%Y-%m-%d') for trade in trades]
        values = [trade['tradeAmount'] for trade in trades]
        return dates, values
    else:
        return None, None

def fetch_fear_and_greed():
    url = "https://api.alternative.me/fng/?limit=365"
    response = requests.get(url)
    data = response.json()
    
    if data and 'data' in data:
        dates = [datetime.fromtimestamp(int(entry['timestamp'])) for entry in data['data']]
        values = [int(entry['value']) for entry in data['data']]
        return dates, values
    
    return None, None

def create_chart(dates, values, title, ylabel):
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(dates, values, marker='o', linestyle='-', color='b', linewidth=2)
    
    ax.set_title(title)
    ax.set_xlabel('Date')
    ax.set_ylabel(ylabel)
    
    ax.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close(fig)
    
    return buf

def fetch_total_market_cap_chart():
    dates, values = fetch_total_market_cap()
    
    if dates is None or values is None:
        return None
    
    return create_chart(dates, values, 'Total Market Cap', 'Market Cap (USD)')

def fetch_bitcoin_dominance_chart():
    dates, values = fetch_bitcoin_dominance()
    
    if dates is None or values is None:
        return None
    
    return create_chart(dates, values, 'Bitcoin Dominance', 'Dominance (%)')

def fetch_defi_market_cap_chart():
    dates, values = fetch_defi_market_cap()
    
    if dates is None or values is None:
        return None
    
    return create_chart(dates, values, 'DeFi Market Cap', 'Market Cap (USD)')

def fetch_fear_and_greed_chart():
    dates, values = fetch_fear_and_greed()
    
    if dates is None or values is None:
        return None
    
    return create_chart(dates, values, 'Fear and Greed Index', 'Index Value')