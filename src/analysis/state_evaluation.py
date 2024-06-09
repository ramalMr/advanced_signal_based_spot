import pandas as pd
from typing import Tuple

def find_empirical_values(indicator: pd.Series, quantile: float) -> Tuple[float, float]:
    """
    verilen gosterici ucun asagidaki hedleri tapir.
    """
    bottom_threshold = indicator.quantile(1 - quantile)
    peak_threshold = indicator.quantile(quantile)
    return bottom_threshold, peak_threshold

def evaluate_current_state(correlations: list, current_values: list, thresholds: list) -> float:
    """
    Korrelyasiyalar cari gosterici deyerleri ve hedlere gore cari veziyyeti qiymetlendirir
    """
    state = 0.0
    for correlation, current_value, threshold in zip(correlations, current_values, thresholds):
        if current_value < threshold[0]:
            state += correlation * -1
        elif current_value > threshold[1]:
            state += correlation
    return state