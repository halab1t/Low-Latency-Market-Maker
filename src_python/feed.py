import time
import pandas as pd

class MarketDataFeed:
    def __init__(self, data_path):
        self.data = pd.read_csv(data_path)
    
    def stream(self):
        """Yield one tick at a time with simulated delay"""
        for _, row in self.data.iterrows():
            tick = {
                "ts": time.time_ns(),
                "bid": row["bid"],
                "ask": row["ask"],
                "last": row["last_price"],
                "size": row["size"]
            }
            yield tick
            time.sleep(0.001)  # simulate 1ms between ticks

