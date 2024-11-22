import unittest
import pandas as pd
import numpy as np
from src.analysis.correlation import calculate_correlation, calculate_correlations
from src.analysis.state_evaluation import find_empirical_values, evaluate_current_state

class TestAnalysis(unittest.TestCase):
    def setUp(self):
        self.data = pd.DataFrame({
            'close': np.random.randn(100).cumsum() + 100,
            'macd': np.random.randn(100),
            'rsi': np.random.uniform(0, 100, 100),
            'volume_imbalance': np.random.randn(100)
        })

    def test_calculate_correlation(self):
        corr = calculate_correlation(self.data['close'], self.data['macd'])
        self.assertIsInstance(corr, float)
        self.assertTrue(-1 <= corr <= 1)

    def test_calculate_correlations(self):
        corrs = calculate_correlations(self.data)
        self.assertIsInstance(corrs, dict)
        self.assertTrue(all(key in corrs for key in ['macd', 'rsi', 'volume_imbalance']))

    def test_find_empirical_values(self):
        lower, upper = find_empirical_values(self.data['macd'])
        self.assertLess(lower, upper)

    def test_evaluate_current_state(self):
        correlations = calculate_correlations(self.data)
        empirical_values = {col: find_empirical_values(self.data[col]) for col in ['macd', 'rsi', 'volume_imbalance']}
        state, probability = evaluate_current_state(self.data.iloc[-1], correlations, empirical_values)
        self.assertIn(state, ['bullish', 'bearish', 'neutral'])
        self.assertTrue(0 <= probability <= 1)

if __name__ == '__main__':
    unittest.main()