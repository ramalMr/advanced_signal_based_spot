import pandas as pd
import numpy as np
from src.backtesting.backtest import Backtester

def generate_price_pattern(pattern_type: str, length: int = 1000, start_price: float = 1000.0) -> pd.DataFrame:
    date_range = pd.date_range(start='2024-01-01', periods=length, freq='H')
    data = pd.DataFrame(index=date_range, columns=['open', 'high', 'low', 'close', 'volume'])
    
    if pattern_type == 'uptrend':
        data['close'] = np.linspace(start_price, start_price * 1.5, length)
    elif pattern_type == 'downtrend':
        data['close'] = np.linspace(start_price, start_price * 0.5, length)
    elif pattern_type == 'sideways':
        data['close'] = np.random.normal(start_price, start_price * 0.02, length)
    elif pattern_type == 'volatile_up':
        trend = np.linspace(0, 1, length)
        noise = np.random.normal(0, 0.1, length)
        data['close'] = start_price * (1 + trend + noise)
    elif pattern_type == 'volatile_down':
        trend = np.linspace(0, -1, length)
        noise = np.random.normal(0, 0.1, length)
        data['close'] = start_price * (1 + trend + noise)
    #elaveler
    
    data['open'] = data['close'].shift(1)
    data['high'] = data['close'] * (1 + abs(np.random.normal(0, 0.01, length)))
    data['low'] = data['close'] * (1 - abs(np.random.normal(0, 0.01, length)))
    data['volume'] = np.random.normal(1000000, 200000, length)
    
    return data.dropna()

def test_pattern(backtester: Backtester, pattern_type: str) -> dict:
    data = generate_price_pattern(pattern_type)
    backtester.data_loader.load_historical_data = lambda: data
    
    param_grid = {
        'macd_fast': [12, 26],
        'macd_slow': [26, 52],
        'macd_signal': [9, 18],
        'rsi_period': [14, 28],
        'vol_imbalance_period': [14, 28],
        'bb_period': [20, 40],
        'bb_std': [2, 2.5],
        'atr_period': [14, 28],
        'trend_period': [50, 100],
        'entry_threshold': [0.6, 0.7],
        'stop_loss_pct': [0.02, 0.03],
        'take_profit_pct': [0.04, 0.06]
    }
    
    best_params, best_performance = backtester.optimize_parameters(param_grid)
    
    return {
        'pattern': pattern_type,
        'best_params': best_params,
        'performance': best_performance
    }

def run_pattern_tests():
    backtester = Backtester('BTCUSDT', '1h', 1000)
    patterns = ['uptrend', 'downtrend', 'sideways', 'volatile_up', 'volatile_down']
    results = []
    
    for pattern in patterns:
        result = test_pattern(backtester, pattern)
        results.append(result)
        print(f"Pattern: {pattern}")
        print(f"Best Parameters: {result['best_params']}")
        print(f"Performance:")
        for key, value in result['performance'].items():
            print(f"  {key}: {value}")
        print("------------------------")
    
    return results

if __name__ == '__main__':
    results = run_pattern_tests()
    