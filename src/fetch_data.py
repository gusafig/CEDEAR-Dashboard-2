import yfinance as yf
import json
import os
from datetime import datetime

# Usa una lista corta primero para probar que funciona
CEDEARS = {
    "AAPL": {"name": "Apple", "ratio": 20},
    "MSFT": {"name": "Microsoft", "ratio": 30},
    "KO": {"name": "Coca-Cola", "ratio": 5},
    "TSLA": {"name": "Tesla", "ratio": 15}
}

def main():
    tickers = list(CEDEARS.keys())
    # Descarga masiva (evita bloqueos)
    data = yf.download(tickers, period="1y", interval="1d", group_by='ticker')
    
    dict_final = {}
    for ticker in tickers:
        try:
            df = data[ticker].dropna()
            if df.empty: continue
            
            last_price = df['Close'].iloc[-1]
            prev_price = df['Close'].iloc[-2]
            
            dict_final[ticker] = {
                "name": CEDEARS[ticker]["name"],
                "price_usd": round(float(last_price), 2),
                "change_pct": round(float(((last_price/prev_price)-1)*100), 2),
                "ratio": CEDEARS[ticker]["ratio"],
                "last_update": datetime.now().strftime("%H:%M")
            }
        except:
            continue

    os.makedirs("data", exist_ok=True)
    with open("data/market_data.json", "w") as f:
        json.dump({"tickers": dict_final}, f, indent=4)

if __name__ == "__main__":
    main()
