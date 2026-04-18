from flask import Flask, render_template, request
import yfinance as yf
import matplotlib
matplotlib.use('Agg')  
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/stock", methods=["POST"])
def stock():
    symbol = request.form["symbol"]

    data = yf.download(symbol, period="6mo")

    if data.empty:
        return "Invalid stock symbol"

    # Create chart
    plt.figure()
    data["Close"].plot(title=f"{symbol} Stock Price")

    plt.xticks(rotation=45)
    plt.tight_layout()

    # Ensure static folder exists
    if not os.path.exists("static"):
        os.makedirs("static")

    img_path = os.path.join("static", "chart.png")
    plt.savefig(img_path)
    plt.close()

    return render_template("result.html", symbol=symbol)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)