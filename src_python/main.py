import json
import socket
import time

from feed import MarketDataFeed
from order_book import OrderBook
from strategy import MarketMakerStrategy
from execution import ExecutionEngine
from risk import RiskManager
from fill_simulator import simulate_fills, mark_to_market

def run_engine(socket_conn, data_path="data/first_sample_ticks.csv"):
    feed = MarketDataFeed(data_path)
    book = OrderBook()
    strategy = MarketMakerStrategy(spread=0.04, qty=2)
    exec_engine = ExecutionEngine()
    risk = RiskManager(max_inventory=50)

    cash = 0.0
    inventory = 0
    tick_num = 0

    for tick in feed.stream():
        tick_num += 1
        bid = tick["bid"]
        ask = tick["ask"]
        mid = (bid + ask) / 2

        book.update_from_tick(tick)
        orders = strategy.on_tick(book)
        orders = risk.adjust_orders(orders)

        # Use separate fill simulator
        cash, inventory = simulate_fills(orders, mid, cash, inventory)

        # Send to execution engine (placeholder)
        for o in orders:
            exec_engine.send_order(o)

        pnl = mark_to_market(cash, inventory, mid)

        msg = {
            "tick": tick_num,
            "pnl": pnl,
            "best_bid": bid,
            "best_ask": ask,
            "my_bid": orders[0]["price"] if orders else None,
            "my_ask": orders[1]["price"] if len(orders) > 1 else None,
            "inventory": inventory
        }
        socket_conn.sendall((json.dumps(msg) + "\n").encode())
        time.sleep(0.05)

if __name__ == "__main__":
    HOST, PORT = "127.0.0.1", 9999
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(1)
        print(f"[ENGINE] Listening on {HOST}:{PORT} ...")
        conn, addr = s.accept()
        with conn:
            print(f"[ENGINE] UI connected from {addr}")
            run_engine(conn)

