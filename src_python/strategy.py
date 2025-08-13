import time

class MarketMakerStrategy:
    def __init__(self, spread=0.05, qty=1):
        self.spread = spread
        self.qty = qty

    def on_tick(self, order_book):
        bid, ask = order_book.get_best_prices()
        if bid is None or ask is None:
            return []
        
        mid = (bid + ask) / 2
        return [
            {"side": "B", "price": mid - self.spread/2, "qty": self.qty, "ts": time.time_ns()},
            {"side": "S", "price": mid + self.spread/2, "qty": self.qty, "ts": time.time_ns()}
        ]

