import pandas as pd
import numpy as np

def calculate_bollinger_bands(data: pd.DataFrame, period: int = 20, num_std: float = 2.0) -> pd.DataFrame:
    """
    :param data: Price melumatlar DF
    :param period: ortalama period
    :param num_std: Std
    :return: BB DataF
    """
    typical_price = (data['high'] + data['low'] + data['close']) / 3
    middle_band = typical_price.rolling(window=period).mean()
    std_dev = typical_price.rolling(window=period).std()
    
    upper_band = middle_band + (std_dev * num_std)
    lower_band = middle_band - (std_dev * num_std)
    
    return pd.DataFrame({
        'upper_band': upper_band,
        'middle_band': middle_band,
        'lower_band': lower_band
    })