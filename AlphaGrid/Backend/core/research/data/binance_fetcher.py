import requests
import csv
import os
import time

def fetch_binance_klines(symbol="BTCUSDT", interval="1h", start_time_ms=1704067200000, end_time_ms=1711929600000, output_path="WF-BTCUSDT-2024Q1.csv"):
    """
    Fetches real historical klines from Binance public API.
    Q1 2024: Jan 1, 2024 (1704067200000) to Mar 31, 2024 (1711929600000)
    """
    print(f"Fetching {symbol} {interval} data from Binance...")
    url = "https://api.binance.com/api/v3/klines"
    
    all_klines = []
    current_start = start_time_ms
    limit = 1000
    
    while current_start < end_time_ms:
        params = {
            "symbol": symbol,
            "interval": interval,
            "startTime": current_start,
            "endTime": end_time_ms,
            "limit": limit
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if not data:
                break
                
            all_klines.extend(data)
            current_start = data[-1][0] + 1 # Next candle start time
            
            # Rate limit respect
            time.sleep(0.1)
        except Exception as e:
            print(f"API Error: {e}")
            break
            
    print(f"Fetched {len(all_klines)} candles.")
    
    # Save to CSV
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with open(output_path, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "open", "high", "low", "close", "volume"])
        for k in all_klines:
            writer.writerow([k[0], k[1], k[2], k[3], k[4], k[5]])
            
    return os.path.abspath(output_path)

if __name__ == "__main__":
    out_path = os.path.join(os.path.dirname(__file__), "WF-BTCUSDT-2024Q1.csv")
    fetch_binance_klines(output_path=out_path)
    print(f"Data saved to {out_path}")
