import unittest
import pandas as pd
from src.indicators.macd import calculate_macd
from src.indicators.rsi import calculate_rsi
from src.indicators.volume_imbalance import calculate_volume_imbalance

class TestIndicators(unittest.TestCase):
    def setUp(self):
        self.data = pd.DataFrame({
            'close': [100, 110, 120, 130, 140],
            'volume': [1000, 2000, 3000, 4000, 5000]
        })
    
    def test_calculate_macd(self):
        macd, signal = calculate_macd(self.data, 2, 3, 2)
        self.assertIsNotNone(macd)
        self.assertIsNotNone(signal)
        self.assertEqual(len(macd), len(self.data))
        self.assertEqual(len(signal), len(self.data))
    
    def test_calculate_rsi(self):
        rsi = calculate_rsi(self.data, 2)
        self.assertIsNotNone(rsi)
        self.assertEqual(len(rsi), len(self.data))
    
    def test_calculate_volume_imbalance(self):
        volume_imbalance = calculate_volume_imbalance(self.data, 2)
        self.assertIsNotNone(volume_imbalance)
        self.assertEqual(len(volume_imbalance), len(self.data))
    def calculate_macd(data: pd.DataFrame, short_period: int, long_period: int, signal_period: int) -> tuple[pd.Series, pd.Series]:
        exp1 = data['close'].ewm(span=short_period, adjust=False).mean()
        exp2 = data['close'].ewm(span=long_period, adjust=False).mean()
        macd = exp1 - exp2
        signal = macd.ewm(span=signal_period, adjust=False).mean()
        return macd, signal

    def calculate_rsi(data: pd.DataFrame, period: int) -> pd.Series:
        delta = data['close'].diff()
        up = delta.clip(lower=0)
        down = -delta.clip(upper=0)
        ma_up = up.rolling(window=period).mean()
        ma_down = down.rolling(window=period).mean()
        rs = ma_up / ma_down
        rsi = 100 - (100 / (1 + rs))
        return rsi

    def calculate_volume_imbalance(data: pd.DataFrame) -> pd.Series:
        volume_imbalance = data['taker_buy_base_asset_volume'] - (data['volume'] - data['taker_buy_base_asset_volume'])
        return volume_imbalance