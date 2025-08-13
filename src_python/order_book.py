class OrderBook:
    def __init__(self):
        self.best_bid = None
        self.best_ask = None

    def update_from_tick(self, tick):
        self.best_bid = tick["bid"]
        self.best_ask = tick["ask"]

    def get_best_prices(self):
        return self.best_bid, self.best_ask

