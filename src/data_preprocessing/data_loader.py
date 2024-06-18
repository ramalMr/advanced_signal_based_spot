import pandas as pd
from typing import List
from binance.client import Client
from src.utils.config import BINANCE_API_KEY, BINANCE_SECRET_KEY

class DataLoader:
    def __init__(self, symbol: str, interval: str, limit: int):
        self.symbol = symbol
        self.interval = interval
        self.limit = limit
        self.client = Client(BINANCE_API_KEY, BINANCE_SECRET_KEY)
    
    def load_data(self) -> pd.DataFrame:
        """
        Binance API-den melumatlar yukleyir 
        """
        klines = self.client.get_klines(symbol=self.symbol, interval=self.interval, limit=self.limit)
        data = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
        data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')
        # Set timezone to UTC
        data['timestamp'] = data['timestamp'].dt.tz_localize('UTC')

        data.set_index('timestamp', inplace=True)
        data = data[['open', 'high', 'low', 'close', 'volume']]
        data = data.astype(float)
        return data