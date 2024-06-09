import pandas as pd
import numpy as np

def calculate_volume_imbalance(data: pd.DataFrame, period: int) -> pd.Series:
    """
    Verilmis melumatlar uçun həcm oynamsini hesablayir.
    """
    volume_imbalance = data['volume'] - data['volume'].rolling(window=period).mean()
    volume_imbalance = pd.Series(volume_imbalance, index=data.index)  # error np.ndarray >> pd.Series 
    volume_imbalance = volume_imbalance.fillna(0)
    volume_imbalance = volume_imbalance.replace([np.inf, -np.inf], 0)
    return volume_imbalance