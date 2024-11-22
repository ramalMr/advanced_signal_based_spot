import pandas as pd
import numpy as np
import itertools
from typing import Tuple, List, Dict
from src.data_preprocessing.data_loader import DataLoader
from src.indicators.macd import calculate_macd
from src.indicators.rsi import calculate_rsi
from src.indicators.volume_imbalance import calculate_volume_imbalance
from src.indicators.bollinger_bands import calculate_bollinger_bands
from src.indicators.atr import calculate_atr
from src.analysis.correlation import calculate_correlations
from src.analysis.state_evaluation import find_empirical_values, evaluate_current_state

class Backtester:
    def __init__(self, symbol: str, interval: str, limit: int, initial_capital: float = 10000, stop_loss: float = 0.02, take_profit: float = 0.04):
        self.symbol = symbol
        self.interval = interval
        self.limit = limit
        self.data_loader = DataLoader(symbol, interval, limit)
        self.initial_capital = initial_capital
        self.stop_loss = stop_loss
        self.take_profit = take_profit
    def backtest(self, params: Dict[str, any]) -> pd.DataFrame:
        data = self.data_loader.load_historical_data()
        data['macd'], data['signal'], _ = calculate_macd(data, params['macd_fast'], params['macd_slow'], params['macd_signal'])
        data['rsi'] = calculate_rsi(data, params['rsi_period'])
        data['volume_imbalance'] = calculate_volume_imbalance(data, params['vol_imbalance_period'])
        bb_data = calculate_bollinger_bands(data, params['bb_period'], params['bb_std'])
        data = pd.concat([data, bb_data], axis=1)
        data['atr'] = calculate_atr(data, params['atr_period'])
        
        data['trend'] = np.where(data['close'] > data['close'].rolling(window=params['trend_period']).mean(), 1, -1)
        
        data = data.dropna()
        
        correlations = calculate_correlations(data)
        print("Correlations:", correlations)
        
        empirical_values = {}
        for column in ['macd', 'rsi', 'volume_imbalance']:
            empirical_values[column] = find_empirical_values(data[column])
        print("Empirical values:", empirical_values)
        
        data['trend'], data['probability'] = zip(*data.apply(
            lambda row: evaluate_current_state(row, correlations, empirical_values), axis=1
        ))
        
        data['signal'] = 0
        data['position'] = 0
        data['entry_price'] = 0
        data['stop_loss'] = 0
        data['take_profit'] = 0
        
        for i in range(1, len(data)):
            if data['position'].iloc[i-1] == 0:
                if data['trend'].iloc[i] == 'bullish' and data['probability'].iloc[i] > params['entry_threshold']:
                    data.loc[data.index[i], 'signal'] = 1
                    data.loc[data.index[i], 'position'] = 1
                    data.loc[data.index[i], 'entry_price'] = data['close'].iloc[i]
                    data.loc[data.index[i], 'stop_loss'] = data['close'].iloc[i] - (data['atr'].iloc[i] * params['stop_loss_multiplier'])
                    data.loc[data.index[i], 'take_profit'] = data['close'].iloc[i] + (data['atr'].iloc[i] * params['take_profit_multiplier'])
                elif data['trend'].iloc[i] == 'bearish' and data['probability'].iloc[i] > params['entry_threshold']:
                    data.loc[data.index[i], 'signal'] = -1
                    data.loc[data.index[i], 'position'] = -1
                    data.loc[data.index[i], 'entry_price'] = data['close'].iloc[i]
                    data.loc[data.index[i], 'stop_loss'] = data['close'].iloc[i] + (data['atr'].iloc[i] * params['stop_loss_multiplier'])
                    data.loc[data.index[i], 'take_profit'] = data['close'].iloc[i] - (data['atr'].iloc[i] * params['take_profit_multiplier'])
            else:
                if (data['position'].iloc[i-1] == 1 and (data['close'].iloc[i] <= data['stop_loss'].iloc[i-1] or data['close'].iloc[i] >= data['take_profit'].iloc[i-1])) or \
                   (data['position'].iloc[i-1] == -1 and (data['close'].iloc[i] >= data['stop_loss'].iloc[i-1] or data['close'].iloc[i] <= data['take_profit'].iloc[i-1])):
                    data.loc[data.index[i], 'signal'] = 0
                    data.loc[data.index[i], 'position'] = 0
                else:
                    data.loc[data.index[i], 'position'] = data['position'].iloc[i-1]
                    data.loc[data.index[i], 'entry_price'] = data['entry_price'].iloc[i-1]
                    data.loc[data.index[i], 'stop_loss'] = data['stop_loss'].iloc[i-1]
                    data.loc[data.index[i], 'take_profit'] = data['take_profit'].iloc[i-1]
        
        data['profit'] = 0.0
        for i in range(1, len(data)):
            if data['position'].iloc[i-1] != 0 and data['position'].iloc[i] == 0:
                if data['position'].iloc[i-1] == 1:
                    data.loc[data.index[i], 'profit'] = (data['close'].iloc[i] - data['entry_price'].iloc[i-1]) / data['entry_price'].iloc[i-1]
                else:
                    data.loc[data.index[i], 'profit'] = (data['entry_price'].iloc[i-1] - data['close'].iloc[i]) / data['entry_price'].iloc[i-1]
        
        data['cumulative_profit'] = data['profit'].cumsum()
        data['capital'] = self.initial_capital * (1 + data['cumulative_profit'])
        
        return data
    def calculate_profit(self, data: pd.DataFrame) -> Dict[str, float]:
        total_profit = data['capital'].iloc[-1] - self.initial_capital
        profit_percentage = (total_profit / self.initial_capital) * 100
        max_drawdown = (data['capital'].cummax() - data['capital']) / data['capital'].cummax()
        sharpe_ratio = np.sqrt(252) * data['profit'].mean() / data['profit'].std() if data['profit'].std() != 0 else 0
        sortino_ratio = np.sqrt(252) * data['profit'].mean() / data['profit'][data['profit'] < 0].std() if data['profit'][data['profit'] < 0].std() != 0 else 0
        trade_count = (data['signal'] != 0).sum()

        return {
            'total_profit': float(total_profit),
            'profit_percentage': float(profit_percentage),
            'max_drawdown': float(max_drawdown.max() * 100),
            'sharpe_ratio': float(sharpe_ratio),
            'sortino_ratio': float(sortino_ratio),
            'trade_count': int(trade_count)
        }

    def optimize_parameters(self, param_grid: Dict[str, List[any]]) -> Tuple[Dict[str, any], Dict[str, float]]:
        best_performance = {'sharpe_ratio': float('-inf')}
        best_params = {}
        
        for params in self._generate_param_combinations(param_grid):
            result = self.backtest(params)
            performance = self.calculate_profit(result)
            
            if performance['sharpe_ratio'] > best_performance['sharpe_ratio']:
                best_performance = performance
                best_params = params
        
        return best_params, best_performance

    def _generate_param_combinations(self, param_grid):
        keys = list(param_grid.keys())
        values = list(param_grid.values())
        for combination in itertools.product(*values):
            yield dict(zip(keys, combination))
    def analyze_results(self, data: pd.DataFrame) -> Dict[str, any]:
        total_trades = (data['signal'] != 0).sum()
        winning_trades = (data['profit'] > 0).sum()
        losing_trades = (data['profit'] < 0).sum()
        win_rate = winning_trades / total_trades if total_trades > 0 else 0

        total_profit = data['profit'].sum()
        average_profit = data['profit'].mean()
        profit_factor = abs(data['profit'][data['profit'] > 0].sum() / data['profit'][data['profit'] < 0].sum()) if data['profit'][data['profit'] < 0].sum() != 0 else float('inf')
    
        max_drawdown = (data['capital'].cummax() - data['capital']).max() / data['capital'].cummax().max()
        
        sharpe_ratio = np.sqrt(365) * data['profit'].mean() / data['profit'].std() if data['profit'].std() != 0 else 0
        sortino_ratio = np.sqrt(365) * data['profit'].mean() / data['profit'][data['profit'] < 0].std() if data['profit'][data['profit'] < 0].std() != 0 else 0

        return {
            'total_trades': total_trades,
            'winning_trades': winning_trades,
            'losing_trades': losing_trades,
            'win_rate': win_rate,
            'total_profit': total_profit,
            'average_profit': average_profit,
            'profit_factor': profit_factor,
            'max_drawdown': max_drawdown,
            'sharpe_ratio': sharpe_ratio,
            'sortino_ratio': sortino_ratio,
            'final_capital': data['capital'].iloc[-1],
            'total_return': (data['capital'].iloc[-1] - self.initial_capital) / self.initial_capital
        }
        