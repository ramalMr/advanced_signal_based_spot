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
