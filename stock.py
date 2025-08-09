import yfinance as yf
import time
from datetime import datetime
import matplotlib.pyplot as plt

SYMBOL = "AAPL"  # Stock ticker
LOW_THRESHOLD = 140.0
HIGH_THRESHOLD = 170.0
CHECK_INTERVAL = 10  # seconds (changed for quick testing)
PLOT_HISTORY_PERIOD = "1mo"  # 1mo, 3mo, 6mo, 1y

def get_price(symbol):
    """Fetch the latest closing price."""
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period="1d", interval="1m")
        return data['Close'].iloc[-1]
    except Exception as e:
        print(f"Error fetching price: {e}")
        return None

def plot_price(symbol, period):
    """Plot stock price over the given period."""
    data = yf.Ticker(symbol).history(period=period)
    plt.figure(figsize=(8, 4))
    plt.plot(data.index, data['Close'], label='Close Price', color='blue')
    plt.title(f"{symbol} Price History ({period})")
    plt.xlabel("Date")
    plt.ylabel("Price (USD)")
    plt.legend()
    plt.grid(True)
    plt.show()

def monitor_stock():
    """Main loop to monitor the stock."""
    print(f"Tracking {SYMBOL}... Press Ctrl+C to stop.")
    while True:
        price = get_price(SYMBOL)
        if price:
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {SYMBOL} Price: ${price:.2f}")
            if price <= LOW_THRESHOLD:
                print(f"🔻 ALERT: {SYMBOL} dropped below ${LOW_THRESHOLD}!")
            elif price >= HIGH_THRESHOLD:
                print(f"🚀 ALERT: {SYMBOL} rose above ${HIGH_THRESHOLD}!")
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    # First, show a chart
    plot_price(SYMBOL, PLOT_HISTORY_PERIOD)
    # Then start monitoring
    monitor_stock()
