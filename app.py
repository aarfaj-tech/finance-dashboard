from flask import Flask, render_template, request
import yfinance as yf
import matplotlib.pyplot as plt
import os

app = Flask(__name__)
os.makedirs("static", exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def dashboard():

    stocks = ["AAPL", "TSLA", "MSFT"]
    selected = "AAPL"
    shares = 0

    if request.method == "POST":
        selected = request.form["stock"].upper()
        shares = float(request.form.get("shares", 0))

    data = yf.Ticker(selected)
    hist = data.history(period="1mo")

    price = round(hist["Close"].iloc[-1], 2)
    change = round(((hist["Close"].iloc[-1] - hist["Close"].iloc[0]) / hist["Close"].iloc[0]) * 100, 2)

    # 📊 CLEAN CHART FIX
    plt.figure(figsize=(8,4))
    plt.plot(hist.index, hist["Close"])
    plt.xticks(rotation=45)
    plt.tight_layout()

    chart_path = "static/chart.png"
    plt.savefig(chart_path)
    plt.close()

    # 💰 portfolio value
    portfolio_value = round(price * shares, 2)

    return render_template(
        "index.html",
        stock=selected,
        price=price,
        change=change,
        chart=chart_path,
        portfolio_value=portfolio_value,
        shares=shares,
        stocks=stocks
    )

if __name__ == "__main__":
    app.run(debug=True)