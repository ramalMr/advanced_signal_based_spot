from scipy.stats import pearsonr
import pandas as pd

def calculate_correlation(price: pd.Series, indicator: pd.Series) -> float:
    """
   qiymet ve verilmis gosterici arasindaki korrelyasiyani hesablayir.
    """
    correlation, _ = pearsonr(price, indicator)
    return correlation
