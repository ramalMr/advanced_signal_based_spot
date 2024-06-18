import datetime
from zoneinfo import ZoneInfo

import pytz
from dateutil.relativedelta import relativedelta
from tzlocal import get_localzone

from src.analysis.correlation import calculate_correlation
from src.analysis.state_evaluation import find_empirical_values, evaluate_current_state
from src.data_preprocessing.data_loader import DataLoader
from src.indicators.macd import calculate_macd
from src.indicators.rsi import calculate_rsi
from src.indicators.volume_imbalance import calculate_volume_imbalance


def analyze_data(data, start_date=None, end_date=None):
    if start_date and end_date:
        data_subset = data.loc[start_date:end_date]
    else:
        data_subset = data
    
    if len(data_subset) < 1:
        return "yeterli melumat yoxdur"
    
    macd, signal = calculate_macd(data_subset, 12, 26, 9)
    rsi = calculate_rsi(data_subset, 14)
    volume_imbalance = calculate_volume_imbalance(data_subset, 2)

    print(macd)
    print(rsi)

    if len(macd) < 2 or len(rsi) < 2 or len(volume_imbalance) < 2:
        return "yeterli melumat yoxdur"
    
    macd_correlation = calculate_correlation(data_subset['close'], macd)
    rsi_correlation = calculate_correlation(data_subset['close'], rsi)
    #volume_imbalance_correlation = calculate_correlation(data_subset['close'], volume_imbalance)
    volume_correlation = calculate_correlation(data_subset['close'], data_subset['volume'])
    
    macd_bottom, macd_peak = find_empirical_values(macd, 0.05)
    rsi_bottom, rsi_peak = find_empirical_values(rsi, 0.05)
    #volume_imbalance_bottom, volume_imbalance_peak = find_empirical_values(volume_imbalance, 0.05)
    volume_bottom, volume_peak = find_empirical_values(data_subset['volume'], 0.05)
    
    current_macd = macd.iloc[-1]
    current_rsi = rsi.iloc[-1]
    current_volume_imbalance = volume_imbalance.iloc[-1]
    current_volume = data_subset['volume'].iloc[-1]
    
    correlations = [macd_correlation, rsi_correlation, volume_correlation]
    current_values = [current_macd, current_rsi, current_volume_imbalance, current_volume]
    thresholds = [(macd_bottom, macd_peak), (rsi_bottom, rsi_peak), (volume_bottom, volume_peak)]
    current_state = evaluate_current_state(correlations, current_values, thresholds)
    
    if current_state > 0:
        sentiment = f"yukselen ({current_state:.2f}, current_macd= {current_macd:.2f}, current_rsi={current_rsi:.2f}, cvi={current_volume_imbalance:.2f}, cv={current_volume:.2f} )"
    elif current_state < 0:
        sentiment = f"enen ({abs(current_state):.2f}, current_macd= {current_macd:.2f}, current_rsi={current_rsi:.2f}, cvi={current_volume_imbalance:.2f}, cv={current_volume:.2f}  )"
    else:
        sentiment = "neytral"
    
    return sentiment

def main():
    symbol = 'BTCFDUSD' #fdusdusdt
    interval = '1m'
    limit = 1000
    data_loader = DataLoader(symbol, interval, limit)
    data = data_loader.load_data()
    
    #start_date = '2022-05-01'
    #end_date = '2023-05-31'

    # Given start date 2023-08-04 00:00

    start_date = datetime.datetime.strptime('2024-06-17 11:00', '%Y-%m-%d %H:%M')

    # Get the local timezone
    # Get the local timezone
    local_timezone = get_localzone()

    # Make the start_date timezone-aware
    start_date = start_date.replace(tzinfo=local_timezone)
    # Get the current time in the local timezone
    now = datetime.datetime.now(local_timezone)

    while start_date < now:
        # Calculate the end date by adding three months to the start date
        end_date = start_date + relativedelta(minutes=1000)

        # Perform sentiment analysis on the data subset

        sentiment_subset = analyze_data(data, start_date, end_date)

        # Print or store the result as needed
        #print(f"Sentiment analysis from {start_date} to {end_date}: {sentiment_subset}")

        print(f"{start_date}:{end_date} araliginda {symbol} bazarin keyfi: {sentiment_subset}")

        # Move the start date to the next period
        start_date = end_date

    sentiment_overall = analyze_data(data)
    print(f"umumi {symbol} bazarin keyfi: {sentiment_overall}")

if __name__ == '__main__':
    main()
    
    
    
    