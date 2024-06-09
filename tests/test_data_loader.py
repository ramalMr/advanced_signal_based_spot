import unittest
from src.data_preprocessing.data_loader import DataLoader

class TestDataLoader(unittest.TestCase):
    def test_load_data(self):
        data_loader = DataLoader('BTCUSDT', '1d', 1000)
        data = data_loader.load_data()
        self.assertIsNotNone(data)
        self.assertEqual(len(data), 1000)
        self.assertIn('open', data.columns)
        self.assertIn('high', data.columns)
        self.assertIn('low', data.columns)
        self.assertIn('close', data.columns)
        self.assertIn('volume', data.columns)