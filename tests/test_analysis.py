import unittest
import pandas as pd
from src.analysis.correlation import calculate_correlation
from src.analysis.state_evaluation import find_empirical_values, evaluate_current_state

class TestAnalysis(unittest.TestCase):
    def setUp(self):
        self.price = pd.Series([100, 110, 120, 130, 140])
        self.indicator = pd.Series([10, 20, 30, 40, 50])
    
    def test_calculate_correlation(self):
        correlation = calculate_correlation(self.price, self.indicator)
        self.assertIsNotNone(correlation)
        self.assertIsInstance(correlation, float)
        self.assertGreaterEqual(correlation, -1)
        self.assertLessEqual(correlation, 1)
    
    def test_find_empirical_values(self):
        bottom, peak = find_empirical_values(self.indicator, 0.9)  # Change this line
        self.assertIsNotNone(bottom)
        self.assertIsNotNone(peak)
        self.assertIsInstance(bottom, float)
        self.assertIsInstance(peak, float)
        self.assertLess(bottom, peak)
    
    def test_evaluate_current_state(self):
        correlations = [0.5, -0.3, 0.8]
        current_values = [60, 40, 80]
        thresholds = [(20, 80), (30, 70), (40, 90)]
        state = evaluate_current_state(correlations, current_values, thresholds)
        self.assertIsNotNone(state)
        self.assertIsInstance(state, float)