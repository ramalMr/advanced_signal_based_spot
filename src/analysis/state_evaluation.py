import pandas as pd
import numpy as np
from typing import Dict, Tuple

def find_empirical_values(indicator: pd.Series, confidence: float = 0.95) -> Tuple[float, float]:
    mean = indicator.mean()
    std = indicator.std()
    z_score = np.abs(np.random.normal(0, 1, 1000)).mean()  # texmini z-score
    lower_bound = mean - z_score * std
    upper_bound = mean + z_score * std
    return lower_bound, upper_bound

def evaluate_current_state(row: pd.Series, correlations: Dict[str, float], empirical_values: Dict[str, Tuple[float, float]]) -> Tuple[str, float]:
    print(f"Setir emal edilir: {row}")
    print(f"Korrelyasiyalar: {correlations}")
    print(f"Empirik deyerler: {empirical_values}")
    
    state = 0
    total_weight = sum(abs(corr) for corr in correlations.values())
    
    for indicator, correlation in correlations.items():
        if indicator in empirical_values and indicator in row:
            lower_bound, upper_bound = empirical_values[indicator]
            value = row[indicator]
            print(f"{indicator} emal edilir: deyer = {value}, asagi serhed = {lower_bound}, yuxari serhed = {upper_bound}")
            
            if pd.isna(value):
                print(f"Xeberdarliq: {indicator} deyeri NaN-dir")
                continue
            
            if not isinstance(value, (int, float)):
                print(f"Xeberdarliq: {indicator} deyeri ededi deyil: {value}")
                continue
            
            weight = abs(correlation) / total_weight if total_weight != 0 else 0
            
            if value < lower_bound:
                state += weight
                print(f"{indicator} asagi serhedden asagidir, veziyyete {weight} elave edilir")
            elif value > upper_bound:
                state -= weight
                print(f"{indicator} yuxari serhedden yuxaridir, veziyyetden {weight} cixilir")

    # Bollinger Bands siqnallari
    if all(key in row for key in ['close', 'lower_band', 'upper_band']):
        close = row['close']
        lower_band = row['lower_band']
        upper_band = row['upper_band']
        print(f"Bollinger Bandlari: baglanis = {close}, asagi band = {lower_band}, yuxari band = {upper_band}")
        
        if pd.isna(close) or pd.isna(lower_band) or pd.isna(upper_band):
            print("Xeberdarliq: Bezi Bollinger Band deyerleri NaN-dir")
        elif not all(isinstance(x, (int, float)) for x in [close, lower_band, upper_band]):
            print(f"Xeberdarliq: Bollinger Band deyerlerinin hamisi ededi deyil")
        else:
            if close < lower_band:
                state += 0.5
                print("Qiymet asagi Bollinger Bandindan asagidir, veziyyete 0.5 elave edilir")
            elif close > upper_band:
                state -= 0.5
                print("Qiymet yuxari Bollinger Bandindan yuxaridir, veziyyetden 0.5 cixilir")

    probability = abs(state)
    print(f"Son veziyyet: {state}, Ehtimal: {probability}")

    if state > 0:
        return "yukselen", min(probability, 1)
    elif state < 0:
        return "enen", min(probability, 1)
    else:
        return "neytral", 0