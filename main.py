import tkinter as tk
from tkinter import ttk, messagebox
import threading
from src.backtesting.backtest import Backtester
from src.utils.visualization import plot_backtesting_result

class BacktestGUI:
    def __init__(self, master):
        self.master = master
        master.title("TechSphere Backtesting Tools")
        master.geometry("600x500")

        self.create_widgets()

    def create_widgets(self):
        
        ttk.Label(self.master, text="Simvol:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.symbol_var = tk.StringVar(value="BTCUSDT")
        ttk.Entry(self.master, textvariable=self.symbol_var).grid(row=0, column=1, padx=5, pady=5, sticky="we")

        ttk.Label(self.master, text="İnterval:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.interval_var = tk.StringVar(value="1h")
        ttk.Combobox(self.master, textvariable=self.interval_var, 
                     values=["1m", "5m", "15m", "30m", "1h", "4h", "1d"]).grid(row=1, column=1, padx=5, pady=5, sticky="we")

        self.macd_var = tk.BooleanVar(value=True)
        self.rsi_var = tk.BooleanVar(value=True)
        self.volume_imbalance_var = tk.BooleanVar(value=True)
        self.bollinger_bands_var = tk.BooleanVar(value=True)

        ttk.Checkbutton(self.master, text="MACD ", variable=self.macd_var).grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="w")
        ttk.Checkbutton(self.master, text="RSI ", variable=self.rsi_var).grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="w")
        ttk.Checkbutton(self.master, text="Vol ", variable=self.volume_imbalance_var).grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="w")
        ttk.Checkbutton(self.master, text="Bollinger Bands ", variable=self.bollinger_bands_var).grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky="w")

        ttk.Button(self.master, text="Backtest Baslat", command=self.run_backtest).grid(row=6, column=0, columnspan=2, padx=5, pady=20)

        self.result_text = tk.Text(self.master, height=15, width=70)
        self.result_text.grid(row=7, column=0, columnspan=2, padx=5, pady=5)

    def run_backtest(self):
        thread = threading.Thread(target=self._run_backtest_thread)
        thread.start()

    def _run_backtest_thread(self):
        try:
            symbol = self.symbol_var.get()
            interval = self.interval_var.get()
            limit = 1000

            backtester = Backtester(symbol, interval, limit)

            param_grid = {
                'macd_fast': [12, 26],
                'macd_slow': [26, 52],
                'macd_signal': [9, 18],
                'rsi_period': [14, 28],
                'vol_imbalance_period': [14, 28],
                'bb_period': [20, 40],
                'bb_std': [2, 2.5],
                'atr_period': [14, 28],
                'trend_period': [50, 100],
                'entry_threshold': [0.6, 0.7],
                'stop_loss_multiplier': [1.5, 2.0],
                'take_profit_multiplier': [2.0, 2.5]
            }

            self.result_text.insert(tk.END, "Backtest basladi...\n")
            self.master.update_idletasks()

            best_params, best_performance = backtester.optimize_parameters(param_grid)
            
            self.result_text.insert(tk.END, f"en optimal parametrler: {best_params}\n")
            self.master.update_idletasks()

            backtesting_result = backtester.backtest(best_params)
            performance = backtester.calculate_profit(backtesting_result)
            analysis = backtester.analyze_results(backtesting_result)
            
            self.result_text.insert(tk.END, "\nFinal Analiz:\n")
            self.result_text.insert(tk.END, f"umumi ticaret sayi: {analysis['total_trades']}\n")
            self.result_text.insert(tk.END, f"Qazancli ticaretler: {analysis['winning_trades']}\n")
            self.result_text.insert(tk.END, f"Zererli ticaretler: {analysis['losing_trades']}\n")
            self.result_text.insert(tk.END, f"Qazanc nisbeti: {analysis['win_rate']:.2%}\n")
            self.result_text.insert(tk.END, f"umumi menfeet: ${analysis['total_profit']:.2f}\n")
            self.result_text.insert(tk.END, f"Ortalama menfeet: ${analysis['average_profit']:.2f}\n")
            self.result_text.insert(tk.END, f"Menfeet faktoru: {analysis['profit_factor']:.2f}\n")
            self.result_text.insert(tk.END, f"Maksimum drawdown: {analysis['max_drawdown']:.2%}\n")
            self.result_text.insert(tk.END, f"Sharpe nisbeti: {analysis['sharpe_ratio']:.2f}\n")
            self.result_text.insert(tk.END, f"Sortino nisbeti: {analysis['sortino_ratio']:.2f}\n")
            self.result_text.insert(tk.END, f"Son kapital: ${analysis['final_capital']:.2f}\n")
            self.result_text.insert(tk.END, f"umumi gelir: {analysis['total_return']:.2%}\n")
            
            self.master.update_idletasks()

            self.master.after(0, lambda: plot_backtesting_result(backtesting_result))

        except Exception as e:
            error_message = f"Xeta bas verdi: {str(e)}\n"
            print(error_message)  
            self.master.after(0, lambda: self.result_text.insert(tk.END, error_message))
            self.master.after(0, lambda m=error_message: messagebox.showerror("Xeta", m))


if __name__ == '__main__':
    root = tk.Tk()
    app = BacktestGUI(root)
    root.mainloop()
