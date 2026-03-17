import yfinance as yf
import json
import pandas as pd
from config import CEDEAR_MAP

def update_market_data():
    tickers = list(CEDEAR_MAP.keys())
    results = {}
    
    print(f"Actualizando {len(tickers)} activos...")
    
    for symbol in tickers:
        try:
            ticker = yf.Ticker(symbol)
            # Pedimos 3 años de datos para indicadores de largo plazo
            hist = ticker.history(period="3y")
            
            if hist.empty: continue
            
            last_close = hist['Close'].iloc[-1]
            change = ((last_close / hist['Close'].iloc[-2]) - 1) * 100
            
            # Indicadores técnicos simples
            sma50 = hist['Close'].rolling(window=50).mean().iloc[-1]
            sma200 = hist['Close'].rolling(window=200).mean().iloc[-1]
            
            results[symbol] = {
                "name": CEDEAR_MAP[symbol]["name"],
                "price": round(last_close, 2),
                "change": round(change, 2),
                "ratio": CEDEAR_MAP[symbol]["ratio"],
                "sma50": round(sma50, 2),
                "sma200": round(sma200, 2),
                "last_update": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M")
            }
        except Exception as e:
            print(f"Error en {symbol}: {e}")

    with open('data/market_data.json', 'w') as f:
        json.dump(results, f, indent=4)

if __name__ == "__main__":
    update_market_data()
