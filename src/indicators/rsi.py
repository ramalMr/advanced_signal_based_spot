import pandas as pd
import numpy as np

def calculate_rsi(data: pd.DataFrame, period: int) -> pd.Series:
    """
    Verilmis melumatlar ucun RSI gostericisi hesablayir.
    """
    delta = data['close'].diff()
    up = delta.clip(lower=0)
    down = -delta.clip(upper=0)
    ma_up = up.rolling(window=period).mean()
    ma_down = down.rolling(window=period).mean()
    rs = np.where(ma_down != 0, ma_up / ma_down, 0)
    rsi = 100 - (100 / (1 + rs))
    rsi = pd.Series(rsi, index=data.index)  
    rsi = rsi.fillna(0)
    rsi = rsi.replace([np.inf, -np.inf], 0)
    return rsi