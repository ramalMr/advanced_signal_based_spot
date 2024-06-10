from src.data_preprocessing.data_loader import DataLoader
from src.indicators.macd import calculate_macd
from src.indicators.rsi import calculate_rsi
from src.indicators.volume_imbalance import calculate_volume_imbalance
from src.analysis.correlation import calculate_correlation
from src.analysis.state_evaluation import find_empirical_values, evaluate_current_state

def analyze_data(data, start_date=None, end_date=None):
    if start_date and end_date:
        data_subset = data.loc[start_date:end_date]
    else:
        data_subset = data
    
    if len(data_subset) < 2:
        return "yeterli melumat yoxdur"
    
    macd, signal = calculate_macd(data_subset, 12, 26, 9)
    rsi = calculate_rsi(data_subset, 14)
    volume_imbalance = calculate_volume_imbalance(data_subset, 20)
    
    if len(macd) < 2 or len(rsi) < 2 or len(volume_imbalance) < 2:
        return "yeterli melumat yoxdur"
    
    macd_correlation = calculate_correlation(data_subset['close'], macd)
    rsi_correlation = calculate_correlation(data_subset['close'], rsi)
    volume_imbalance_correlation = calculate_correlation(data_subset['close'], volume_imbalance)
    volume_correlation = calculate_correlation(data_subset['close'], data_subset['volume'])
    
    macd_bottom, macd_peak = find_empirical_values(macd, 0.05)
    rsi_bottom, rsi_peak = find_empirical_values(rsi, 0.05)
    volume_imbalance_bottom, volume_imbalance_peak = find_empirical_values(volume_imbalance, 0.05)
    volume_bottom, volume_peak = find_empirical_values(data_subset['volume'], 0.05)
    
    current_macd = macd.iloc[-1]
    current_rsi = rsi.iloc[-1]
    current_volume_imbalance = volume_imbalance.iloc[-1]
    current_volume = data_subset['volume'].iloc[-1]
    
    correlations = [macd_correlation, rsi_correlation, volume_imbalance_correlation, volume_correlation]
    current_values = [current_macd, current_rsi, current_volume_imbalance, current_volume]
    thresholds = [(macd_bottom, macd_peak), (rsi_bottom, rsi_peak), (volume_imbalance_bottom, volume_imbalance_peak), (volume_bottom, volume_peak)]
    current_state = evaluate_current_state(correlations, current_values, thresholds)
    
    if current_state > 0:
        sentiment = f"yukselen ({current_state:.2f})"
    elif current_state < 0:
        sentiment = f"enen ({abs(current_state):.2f})"
    else:
        sentiment = "neytral"
    
    return sentiment

def main():
    symbol = 'BTCUSDT' #fdusdusdt
    interval = '1d'
    limit = 1000
    data_loader = DataLoader(symbol, interval, limit)
    data = data_loader.load_data()
    
    start_date = '2022-05-01'
    end_date = '2023-05-31'
    
    sentiment_subset = analyze_data(data, start_date, end_date)
    print(f"2022-05:2023-05 araliginda {symbol} bazarin keyfi: {sentiment_subset}")
    
    sentiment_overall = analyze_data(data)
    print(f"umumi {symbol} bazarin keyfi: {sentiment_overall}")

if __name__ == '__main__':
    main()
    
    
    
    