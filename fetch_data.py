import yfinance as yf
import json
import os
from datetime import datetime

# Ratios extraídos de tu PDF
CEDEARS = {
    "AAPL": {"name": "Apple", "ratio": 20},
    "AMZN": {"name": "Amazon", "ratio": 144},
    "BABA": {"name": "Alibaba", "ratio": 9},
    "KO":   {"name": "Coca-Cola", "ratio": 5},
    "MELI": {"name": "Mercado Libre", "ratio": 120},
    "MSFT": {"name": "Microsoft", "ratio": 30},
    "NVDA": {"name": "NVIDIA", "ratio": 48},
    "TSLA": {"name": "Tesla", "ratio": 15},
    "V":    {"name": "Visa", "ratio": 18},
    "VIST": {"name": "Vista Energy", "ratio": 3}
}

def main():
    tickers = list(CEDEARS.keys())
    # Descargamos datos del último año
    data = yf.download(tickers, period="1y", interval="1d", group_by='ticker')
    
    results = {}
    for sym in tickers:
        try:
            df = data[sym].dropna()
            if df.empty: continue
            
            last_price = df['Close'].iloc[-1]
            prev_price = df['Close'].iloc[-2]
            change = ((last_price / prev_price) - 1) * 100
            
            results[sym] = {
                "name": CEDEARS[sym]["name"],
                "price_usd": round(float(last_price), 2),
                "change_pct": round(float(change), 2),
                "ratio": CEDEARS[sym]["ratio"],
                "last_update": datetime.now().strftime("%d/%m %H:%M")
            }
        except: continue

    os.makedirs("data", exist_ok=True)
    with open("data/market_data.json", "w") as f:
        json.dump({"tickers": results}, f, indent=4)
    print("¡Datos guardados con éxito!")

if __name__ == "__main__":
    main()
