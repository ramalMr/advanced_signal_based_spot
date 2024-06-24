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
    
    def load_historical_data(self) -> pd.DataFrame:
        klines = self.client.get_klines(symbol=self.symbol, interval=self.interval, limit=self.limit)
        data = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
        data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')
        data['timestamp'] = data['timestamp'].dt.tz_localize('UTC')
        data.set_index('timestamp', inplace=True)
        data = data[['open', 'high', 'low', 'close', 'volume']]
        data = data.astype(float)
        data['buy_volume'] = data['volume'] * (data['close'] > data['open']).astype(int)
        data['sell_volume'] = data['volume'] * (data['close'] <= data['open']).astype(int)
        data['volume_imbalance'] = data['buy_volume'] - data['sell_volume']
        return data
    
    def get_real_time_data(self, interval: str):
        try:
            klines = self.client.get_klines(symbol=self.symbol, interval=interval, limit=1000)
            data = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
            data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')
            data.set_index('timestamp', inplace=True)
            data = data[['open', 'high', 'low', 'close', 'volume']]
            data = data.astype(float)
            data['buy_volume'] = data['volume'] * (data['close'] > data['open']).astype(int)
            data['sell_volume'] = data['volume'] * (data['close'] <= data['open']).astype(int)
            data['volume_imbalance'] = data['buy_volume'] - data['sell_volume']
            return data
        except Exception as e:
            print(f"Real-time melumatlari alan zaman error bas verdi: {e}")
            return None