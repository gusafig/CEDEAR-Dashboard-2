import yfinance as yf
import json
import os
import pandas as pd
from datetime import datetime
from config import CEDEAR_MAP

def update_market_data():
    tickers = list(CEDEAR_MAP.keys())
    results = {}
    
    print(f"Descargando datos para {len(tickers)} activos...")
    
    # Descarga masiva para optimizar tiempo
    data = yf.download(tickers, period="3y", interval="1d")['Adj Close']
    
    for symbol in tickers:
        try:
            series = data[symbol].dropna()
            if series.empty: continue
            
            price = series.iloc[-1]
            prev_price = series.iloc[-2]
            change = ((price / prev_price) - 1) * 100
            
            # Indicadores técnicos básicos
            sma50 = series.rolling(window=50).mean().iloc[-1]
            sma200 = series.rolling(window=200).mean().iloc[-1]
            
            results[symbol] = {
                "name": CEDEAR_MAP[symbol]["name"],
                "price_usd": round(float(price), 2),
                "change": round(float(change), 2),
                "ratio": CEDEAR_MAP[symbol]["ratio"],
                "sma50": round(float(sma50), 2) if not pd.isna(sma50) else None,
                "sma200": round(float(sma200), 2) if not pd.isna(sma200) else None,
                "last_update": datetime.now().strftime("%d/%m %H:%M")
            }
        except Exception as e:
            print(f"Error en {symbol}: {e}")

    os.makedirs("data", exist_ok=True)
    with open('data/market_data.json', 'w') as f:
        json.dump(results, f, indent=4)
    print("Market Data actualizado exitosamente.")

if __name__ == "__main__":
    update_market_data()
