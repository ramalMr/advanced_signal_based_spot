import pandas as pd
from typing import Tuple
import numpy as np
def calculate_macd(data: pd.DataFrame, short_period: int, long_period: int, signal_period: int) -> Tuple[pd.Series, pd.Series]:
    """
    Verilmis melumatlar ucun MACD gostericisini hesablayir.
    """
    exp1 = data['close'].ewm(span=short_period, adjust=False).mean()
    exp2 = data['close'].ewm(span=long_period, adjust=False).mean()
    macd = exp1 - exp2
    signal = macd.ewm(span=signal_period, adjust=False).mean()
    macd = macd.fillna(0)
    macd = macd.replace([np.inf, -np.inf], 0)
    signal = signal.fillna(0)
    signal = signal.replace([np.inf, -np.inf], 0)
    return macd, signal
