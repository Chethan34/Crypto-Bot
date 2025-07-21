import os
import requests
from telegram import Update
from telegram.ext import CallbackContext
from dotenv import load_dotenv

load_dotenv()

def fetch_access_token():
    url = "https://oauth2.bitquery.io/oauth2/token"
    payload = {
        'grant_type': 'client_credentials',
        'client_id': os.getenv('BITQUERY_CLIENT_ID'),
        'client_secret': os.getenv('BITQUERY_CLIENT_SECRET'),
        'scope': 'api'
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.post(url, headers=headers, data=payload)
    resp_json = response.json()
    return resp_json.get('access_token', None)

def fetch_transaction_by_hash(tx_hash):
    token = fetch_access_token()
    if not token:
        return None

    url = 'https://streaming.bitquery.io/graphql'

    query = f"""
    query MyQuery {{
      EVM {{
        Transactions(
          where: {{Transaction: {{Hash: {{is: "{tx_hash}"}}}}}}
        ) {{
          Block {{
            Time
            Number
            Nonce
            Hash
          }}
          Transaction {{
            CallCount
            Cost
            CostInUSD
            Data
            From
            Gas
            GasFeeCap
            GasPrice
            GasPriceInUSD
            GasTipCap
            Hash
            Index
            Nonce
            Protected
            To
            Type
            Value
            ValueInUSD
          }}
        }}
      }}
    }}
    """

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    try:
        response = requests.post(url, headers=headers, json={'query': query})
        response.raise_for_status()
        return response.json()['data']['EVM']['Transactions']
    except Exception as e:
        print("Error:", e)
        return None

def format_tx_response(tx):
    t = tx['Transaction']
    b = tx['Block']

    try:
        value_eth = float(t['Value']) / (10**18)
        value_usd = float(t['ValueInUSD'])
        cost_usd = float(t['CostInUSD'])
        gas_price = float(t['GasPrice']) / (10**9)  # gwei
    except:
        value_eth = value_usd = cost_usd = gas_price = 0

    return f"""📄 *Transaction Hash Details*:

🔗 Hash: `{t['Hash']}`
📦 Block #: `{b['Number']}` at `{b['Time']}`
👤 From: `{t['From']}`
📥 To: `{t['To']}`
💰 Value: {value_eth:.4f} ETH (${value_usd:.2f})
⛽ Gas Used: {t['Gas']}
⚡ Gas Price: {gas_price:.2f} Gwei
💸 Total Cost: ${cost_usd:.2f}
📚 Type: {t['Type']}, Protected: {t['Protected']}, Index: {t['Index']}
"""
    
def txhash_handler(update: Update, context: CallbackContext) -> None:
    if not context.args:
        update.message.reply_text("Please provide a transaction hash.\nUsage: /txhash <hash>", parse_mode="Markdown")
        return

    tx_hash = context.args[0]
    update.message.reply_text("🔍 Fetching transaction details...")

    tx_data = fetch_transaction_by_hash(tx_hash)

    if tx_data and len(tx_data) > 0:
        msg = format_tx_response(tx_data[0])
        update.message.reply_text(msg, parse_mode="Markdown")
    else:
        update.message.reply_text("❌ No transaction found for the given hash.")
