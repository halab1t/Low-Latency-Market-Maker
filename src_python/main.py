from feed import MarketDataFeed
from order_book import OrderBook
from strategy import MarketMakerStrategy
from execution import ExecutionEngine
from risk import RiskManager
from metrics import LatencyMetrics
import time

feed = MarketDataFeed("data/first_sample_ticks.csv")
book = OrderBook()
strategy = MarketMakerStrategy()
exec_engine = ExecutionEngine()
risk = RiskManager()
metrics = LatencyMetrics()

for tick in feed.stream():
    t0 = time.time_ns()
    book.update_from_tick(tick)
    orders = strategy.on_tick(book)
    orders = risk.adjust_orders(orders)
    for order in orders:
        exec_engine.send_order(order)
    t1 = time.time_ns()
    metrics.record(t0, t1)

print("Latency stats:", metrics.summary())

