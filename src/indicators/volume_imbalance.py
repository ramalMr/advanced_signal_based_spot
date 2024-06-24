import pandas as pd
import numpy as np

def calculate_volume_imbalance(data: pd.DataFrame, period: int = 14) -> pd.Series:
    volume = data['volume']
    close = data['close']
    
    buy_volume = volume.where(close > close.shift(1), 0)
    sell_volume = volume.where(close < close.shift(1), 0)
    
    buy_volume_ma = buy_volume.rolling(window=period).mean()
    sell_volume_ma = sell_volume.rolling(window=period).mean()
    
    volume_imbalance = (buy_volume_ma - sell_volume_ma) / (buy_volume_ma + sell_volume_ma)
    
    return volume_imbalance