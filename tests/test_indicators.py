import unittest
import pandas as pd
import numpy as np
from src.indicators.macd import calculate_macd
from src.indicators.rsi import calculate_rsi
from src.indicators.volume_imbalance import calculate_volume_imbalance
from src.indicators.bollinger_bands import calculate_bollinger_bands
from src.indicators.atr import calculate_atr

class TestIndicators(unittest.TestCase):
    def setUp(self):
        self.data = pd.DataFrame({
            'open': np.random.randn(100).cumsum() + 100,
            'high': np.random.randn(100).cumsum() + 102,
            'low': np.random.randn(100).cumsum() + 98,
            'close': np.random.randn(100).cumsum() + 100,
            'volume': np.random.randint(1000, 10000, 100)
        })

    def test_calculate_macd(self):
        macd, signal, _ = calculate_macd(self.data, 12, 26, 9)
        self.assertEqual(len(macd), len(self.data))
        self.assertEqual(len(signal), len(self.data))

    def test_calculate_rsi(self):
        rsi = calculate_rsi(self.data, 14)
        self.assertEqual(len(rsi), len(self.data))
        self.assertTrue(all(0 <= val <= 100 for val in rsi if not np.isnan(val)))

    def test_calculate_volume_imbalance(self):
        vol_imbalance = calculate_volume_imbalance(self.data, 14)
        self.assertEqual(len(vol_imbalance), len(self.data))

    def test_calculate_bollinger_bands(self):
        bb = calculate_bollinger_bands(self.data, 20, 2)
        self.assertTrue(all(col in bb.columns for col in ['upper_band', 'middle_band', 'lower_band']))
        self.assertEqual(len(bb), len(self.data))
        self.assert_equal(len(bb),len(self.data))
    def test_calculate_atr(self):
        atr = calculate_atr(self.data, 14)
        self.assertEqual(len(atr), len(self.data))
        self.assertTrue(all(val >= 0 for val in atr if not np.isnan(val)))

if __name__ == '__main__':
    unittest.main()