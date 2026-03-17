import yfinance as yf
import json
import os
from datetime import datetime

# Aquí puse los principales del PDF, podés agregar más luego
CEDEARS = {
    "AAPL": "Apple", "MSFT": "Microsoft", "GOOGL": "Google", 
    "AMZN": "Amazon", "TSLA": "Tesla", "KO": "Coca-Cola",
    "MELI": "Mercado Libre", "NVDA": "NVIDIA", "V": "Visa"
}

def main():
    tickers = list(CEDEARS.keys())
    data = yf.download(tickers, period="1y", interval="1d", group_by='ticker')
    res = {}
    for sym in tickers:
        try:
            df = data[sym].dropna()
            if df.empty: continue
            last = df['Close'].iloc[-1]
            prev = df['Close'].iloc[-2]
            res[sym] = {
                "name": CEDEARS[sym],
                "price_usd": round(float(last), 2),
                "change_pct": round(float(((last/prev)-1)*100), 2),
                "last_update": datetime.now().strftime("%H:%M")
            }
        except: continue
    os.makedirs("data", exist_ok=True)
    with open("data/market_data.json", "w") as f:
        json.dump({"tickers": res}, f, indent=4)

if __name__ == "__main__":
    main()
