from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from config import ALPHA_VANTAGE_API_KEY

class AlphaVantageGraphQLWrapper:
    def __init__(self):
        self.transport = RequestsHTTPTransport(
            url='https://www.alphavantage.co/query',
            use_json=True,
            headers={
                "Content-type": "application/json",
            },
            params={"apikey": ALPHA_VANTAGE_API_KEY}
        )
        self.client = Client(transport=self.transport, fetch_schema_from_transport=True)

    def get_stock_price(self, symbol):
        query = gql('''
        query GetStockPrice($symbol: String!) {
          globalQuote(symbol: $symbol) {
            symbol
            price
            change
            changePercent
          }
        }
        ''')
        
        variables = {"symbol": symbol}
        result = self.client.execute(query, variable_values=variables)
        return result['globalQuote']

    def get_intraday_data(self, symbol):
        query = gql('''
        query GetIntradayData($symbol: String!) {
          timeSeriesIntraday(symbol: $symbol, interval: "5min") {
            datetime
            open
            high
            low
            close
            volume
          }
        }
        ''')
        
        variables = {"symbol": symbol}
        result = self.client.execute(query, variable_values=variables)
        return result['timeSeriesIntraday']

    def get_monthly_data(self, symbol):
        query = gql('''
        query GetMonthlyData($symbol: String!) {
          timeSeriesMonthly(symbol: $symbol) {
            date
            open
            high
            low
            close
            volume
          }
        }
        ''')
        
        variables = {"symbol": symbol}
        result = self.client.execute(query, variable_values=variables)
        return result['timeSeriesMonthly']