from flask import Flask, render_template, request
import yfinance as yf
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import os

app = Flask(__name__)

# ---------------- HOME ----------------
@app.route("/")
def home():
    return render_template("index.html")


# ---------------- STOCK ANALYSIS ----------------
@app.route("/stock", methods=["POST"])
def stock():
    symbol = request.form["symbol"].upper()

    data = yf.download(symbol, period="6mo")

    if data.empty:
        return "Invalid stock symbol"

    # FIX MULTIINDEX ISSUE
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    close = data["Close"].dropna()

    latest_price = float(close.iloc[-1])
    old_price = float(close.iloc[0])

    change = latest_price - old_price
    percent = (change / old_price) * 100

    # ---------------- CHART ----------------
    plt.figure(figsize=(10, 5))
    plt.plot(close.index, close.values, linewidth=2)

    plt.title(f"{symbol} Price (6 Months)")
    plt.xlabel("Date")
    plt.ylabel("Price")

    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))

    plt.xticks(rotation=45)
    plt.tight_layout()

    # save chart
    static_path = os.path.join(os.getcwd(), "static")
    os.makedirs(static_path, exist_ok=True)

    img_path = os.path.join(static_path, "chart.png")
    plt.savefig(img_path)
    plt.close()

    return render_template(
        "result.html",
        symbol=symbol,
        price=round(latest_price, 2),
        change=round(change, 2),
        percent=round(percent, 2)
    )


# ---------------- RUN ----------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)