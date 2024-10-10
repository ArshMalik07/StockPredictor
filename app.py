from flask import Flask, render_template, request
import requests
from datetime import datetime

app = Flask(__name__)

# Function to fetch daily stock data
def fetch_daily_stock_data(stock_symbol, stock_exchange, api_key):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={stock_symbol}.{stock_exchange}&apikey={api_key}&outputsize=full'
    r = requests.get(url)
    return r.json()

# Function to fetch Moving Average
def fetch_moving_average(stock_symbol, api_key, stock_exchange, period):
    url = f'https://www.alphavantage.co/query?function=SMA&symbol={stock_symbol}.{stock_exchange}&interval=daily&time_period={period}&series_type=close&apikey={api_key}'
    r = requests.get(url)
    return r.json()

# Function to fetch Bollinger Bands
def fetch_bollinger_bands(stock_symbol, api_key, stock_exchange, period):
    url = f'https://www.alphavantage.co/query?function=BBANDS&symbol={stock_symbol}.{stock_exchange}&interval=daily&time_period={period}&series_type=close&apikey={api_key}'
    r = requests.get(url)
    return r.json()

# Function to fetch RSI
def fetch_rsi(stock_symbol, api_key, stock_exchange):
    url = f'https://www.alphavantage.co/query?function=RSI&symbol={stock_symbol}.{stock_exchange}&interval=daily&time_period=14&series_type=close&apikey={api_key}'
    r = requests.get(url)
    return r.json()

# Function to fetch ATR (Average True Range)
def fetch_atr(stock_symbol, stock_exchange, api_key):
    url = f'https://www.alphavantage.co/query?function=ATR&symbol={stock_symbol}.{stock_exchange}&interval=daily&time_period=14&apikey={api_key}'
    r = requests.get(url)
    return r.json()

# Function to fetch Volume Moving Average
def fetch_volume_average(stock_symbol, api_key, stock_exchange):
    url = f'https://www.alphavantage.co/query?function=EMA&symbol={stock_symbol}.{stock_exchange}&interval=daily&time_period=50&series_type=volume&apikey={api_key}'
    r = requests.get(url)
    return r.json()

# Function to fetch and return stock data for HTML rendering
def fetch_and_return_stock_data(stock_symbol, stock_exchange, api_key):
    daily_data = fetch_daily_stock_data(stock_symbol, stock_exchange, api_key)
    sma_50 = fetch_moving_average(stock_symbol, api_key, stock_exchange, 50)
    sma_200 = fetch_moving_average(stock_symbol, api_key, stock_exchange, 200)
    bollinger_bands = fetch_bollinger_bands(stock_symbol, api_key, stock_exchange, 20)
    rsi_data = fetch_rsi(stock_symbol, api_key, stock_exchange)
    atr_data = fetch_atr(stock_symbol, stock_exchange, api_key)
    volume_average = fetch_volume_average(stock_symbol, api_key, stock_exchange)

    # Get the current year
    current_year = datetime.now().year
    stock_data = []

    time_series = daily_data.get('Time Series (Daily)', {})
    sma_50_series = sma_50.get('Technical Analysis: SMA', {})
    sma_200_series = sma_200.get('Technical Analysis: SMA', {})
    bollinger_series = bollinger_bands.get('Technical Analysis: BBANDS', {})
    rsi_series = rsi_data.get('Technical Analysis: RSI', {})
    atr_series = atr_data.get('Technical Analysis: ATR', {})
    volume_avg_series = volume_average.get('Technical Analysis: EMA', {})

    for date, stock_info in time_series.items():
        if int(date[:4]) >= (current_year - 5):
            stock_data.append({
                "Date": date,
                "Open": stock_info['1. open'],
                "High": stock_info['2. high'],
                "Low": stock_info['3. low'],
                "Close": stock_info['4. close'],
                "Volume": stock_info['5. volume'],
                "SMA_50": sma_50_series.get(date, {}).get('SMA', 'N/A'),
                "SMA_200": sma_200_series.get(date, {}).get('SMA', 'N/A'),
                "Upper_BB": bollinger_series.get(date, {}).get('Real Upper Band', 'N/A'),
                "Lower_BB": bollinger_series.get(date, {}).get('Real Lower Band', 'N/A'),
                "RSI": rsi_series.get(date, {}).get('RSI', 'N/A'),
                "ATR": atr_series.get(date, {}).get('ATR', 'N/A'),
                "Volume_MA": volume_avg_series.get(date, {}).get('EMA', 'N/A'),
            })
    
    return stock_data

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        stock_symbol = request.form.get("stock_symbol").upper()
        stock_exchange = request.form.get("stock_exchange").upper()  # Corrected to "stock_exchange"
        api_key = "N59MGZMSYA4OE0WN"  # Replace with your Alpha Vantage API key

        # Fetch stock data
        stock_data = fetch_and_return_stock_data(stock_symbol, stock_exchange, api_key)
        return render_template("index.html", stock_data=stock_data, stock_symbol=stock_symbol)
    
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True,port=1310)
