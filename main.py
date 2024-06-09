from src.data_preprocessing.data_loader import DataLoader
from src.indicators.macd import calculate_macd
from src.indicators.rsi import calculate_rsi
from src.indicators.volume_imbalance import calculate_volume_imbalance
from src.analysis.correlation import calculate_correlation
from src.analysis.state_evaluation import find_empirical_values, evaluate_current_state

def main():
    symbol = 'BTCUSDT'
    interval = '1d'
    limit = 1000
    data_loader = DataLoader(symbol, interval, limit)
    data = data_loader.load_data()
    
    macd, signal = calculate_macd(data, 12, 26, 9)
    rsi = calculate_rsi(data, 14)
    volume_imbalance = calculate_volume_imbalance(data, 20)
    
    macd_correlation = calculate_correlation(data['close'], macd)
    rsi_correlation = calculate_correlation(data['close'], rsi)
    volume_correlation = calculate_correlation(data['close'], volume_imbalance)
    
    macd_bottom, macd_peak = find_empirical_values(macd, 0.05)
    rsi_bottom, rsi_peak = find_empirical_values(rsi, 0.05)
    volume_bottom, volume_peak = find_empirical_values(volume_imbalance, 0.05)
    
    current_macd = macd.iloc[-1]
    current_rsi = rsi.iloc[-1]
    current_volume = volume_imbalance.iloc[-1]
    
    correlations = [macd_correlation, rsi_correlation, volume_correlation]
    current_values = [current_macd, current_rsi, current_volume]
    thresholds = [(macd_bottom, macd_peak), (rsi_bottom, rsi_peak), (volume_bottom, volume_peak)]
    current_state = evaluate_current_state(correlations, current_values, thresholds)
    
    if current_state > 0:
        sentiment = f"yukselen ({current_state:.2f})"
    elif current_state < 0:
        sentiment = f"enen ({abs(current_state):.2f})"
    else:
        sentiment = "neytral"
    
    print(f"bazarin keyfi: {sentiment}")

if __name__ == '__main__':
    main()