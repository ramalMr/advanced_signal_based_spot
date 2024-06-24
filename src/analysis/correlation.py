import pandas as pd
import numpy as np
from scipy.stats import pearsonr

def calculate_correlation(price: pd.Series, indicator: pd.Series) -> float:
    # nan deyerleri silirem
    valid = ~(np.isnan(price) | np.isnan(indicator))
    price = price[valid]
    indicator = indicator[valid]
    
    if len(price) > 1 and len(indicator) > 1:
        correlation, _ = pearsonr(price, indicator)
        return correlation
    return 0

def calculate_correlations(data: pd.DataFrame) -> dict[str, float]:
    price = data['close']
    correlations = {}
    for column in ['macd', 'rsi', 'volume_imbalance']:
        if column in data.columns:
            correlations[column] = calculate_correlation(price, data[column])
    print("Calculated correlations:", correlations)
    return correlations