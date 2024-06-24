import matplotlib.pyplot as plt
import pandas as pd
import mplfinance as mpf
import seaborn as sns

def plot_backtesting_result(data: pd.DataFrame):

    fig = plt.figure(figsize=(20, 24))
    gs = fig.add_gridspec(6, 2)

    ax1 = fig.add_subplot(gs[0:2, :])
    mpf.plot(data, type='candle', style='charles', ax=ax1, volume=fig.add_subplot(gs[2, :]), 
             title='Qiymet ve Hecm', ylabel='Qiymet')

    # MACD
    ax3 = fig.add_subplot(gs[3, :], sharex=ax1)
    if 'macd' in data.columns and 'signal' in data.columns:
        ax3.plot(data.index, data['macd'], label='MACD')
        ax3.plot(data.index, data['signal'], label='Signal')
        ax3.bar(data.index, data['macd'] - data['signal'], label='Histogram', alpha=0.3)
        ax3.legend()
        ax3.set_ylabel('MACD')

    # RSI
    ax4 = fig.add_subplot(gs[4, :], sharex=ax1)
    if 'rsi' in data.columns:
        ax4.plot(data.index, data['rsi'], label='RSI')
        ax4.axhline(y=30, color='r', linestyle='--')
        ax4.axhline(y=70, color='r', linestyle='--')
        ax4.legend()
        ax4.set_ylabel('RSI')

    # BUY-Sell
    buy_signals = data[data['trend'] == 'bullish']
    sell_signals = data[data['trend'] == 'bearish']
    ax1.scatter(buy_signals.index, buy_signals['low'], marker='^', color='g', s=100, label='Alis')
    ax1.scatter(sell_signals.index, sell_signals['high'], marker='v', color='r', s=100, label='Satis')
    ax1.legend()

    #CE
    ax5 = fig.add_subplot(gs[5, :], sharex=ax1)
    ax5.plot(data.index, data['capital'], label='Kapital')
    ax5.set_ylabel('Kapital')
    ax5.legend()

    plt.tight_layout()
    plt.show()

def plot_profit_distribution(data: pd.DataFrame):
    plt.figure(figsize=(12, 6))
    sns.histplot(data['profit'], kde=True, bins=50)
    plt.title('Ticaret Menfeetlerinin Paylanmasi')
    plt.xlabel('Menfeet')
    plt.ylabel('Tezlik')
    plt.axvline(x=0, color='r', linestyle='--')
    plt.show()

def plot_cumulative_returns(data: pd.DataFrame):
    plt.figure(figsize=(12, 6))
    cumulative_returns = (1 + data['profit']).cumprod() - 1
    plt.plot(data.index, cumulative_returns)
    plt.title('Cumlativ Gelir eyrisi')
    plt.xlabel('Tarix')
    plt.ylabel('Cumlativ Gelir')
    plt.show()

def plot_drawdown(data: pd.DataFrame):
    plt.figure(figsize=(12, 6))
    cumulative_returns = (1 + data['profit']).cumprod() - 1
    running_max = cumulative_returns.cummax()
    drawdown = (cumulative_returns - running_max) / (running_max + 1)
    plt.plot(data.index, drawdown)
    plt.title('Drawdown eyrisi')
    plt.xlabel('Tarix')
    plt.ylabel('Drawdown')
    plt.show()

def plot_monthly_returns(data: pd.DataFrame):
    monthly_returns = data['profit'].resample('M').sum()
    plt.figure(figsize=(12, 6))
    monthly_returns.plot(kind='bar')
    plt.title('Ayliq Gelirler')
    plt.xlabel('Tarix')
    plt.ylabel('Ayliq Gelir')
    plt.xticks(rotation=45)
    plt.show()

def visualize_all_results(data: pd.DataFrame):
    plot_backtesting_result(data)
    plot_profit_distribution(data)
    plot_cumulative_returns(data)
    plot_drawdown(data)
    plot_monthly_returns(data)