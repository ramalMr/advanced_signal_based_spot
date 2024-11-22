import unittest
import pandas as pd
from src.data_preprocessing.data_loader import DataLoader

class TestDataLoader(unittest.TestCase):
    def setUp(self):
        self.data_loader = DataLoader('BTCUSDT', '1h', 1000)

    def test_load_historical_data(self):
        data = self.data_loader.load_historical_data()
        self.assertIsInstance(data, pd.DataFrame)
        self.assertTrue(len(data) > 0)
        self.assertTrue(all(col in data.columns for col in ['open', 'high', 'low', 'close', 'volume']))

    def test_get_real_time_data(self):
        data = self.data_loader.get_real_time_data()
        self.assertIsInstance(data, pd.DataFrame)
        self.assertTrue(len(data) > 0)
        self.assertTrue(all(col in data.columns for col in ['open', 'high', 'low', 'close', 'volume', 'volume_imbalance']))

if __name__ == '__main__':
    unittest.main()