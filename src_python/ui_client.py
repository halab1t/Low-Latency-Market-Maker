import socket
import json
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque

HOST, PORT = "127.0.0.1", 9999

pnl_series = deque(maxlen=5000)
tick_series = deque(maxlen=5000)
bid_series = deque(maxlen=5000)
ask_series = deque(maxlen=5000)
my_bid_series = deque(maxlen=5000)
my_ask_series = deque(maxlen=5000)

def data_listener():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        buffer = ""
        while True:
            data = s.recv(4096).decode()
            if not data:
                break
            buffer += data
            while "\n" in buffer:
                line, buffer = buffer.split("\n", 1)
                yield json.loads(line)

# Matplotlib setup
fig, (ax_pnl, ax_book) = plt.subplots(2, 1, figsize=(10, 7))
pnl_line, = ax_pnl.plot([], [], lw=2)
ax_pnl.set_title("Cumulative PnL")
ax_pnl.set_xlabel("Tick")
ax_pnl.set_ylabel("PnL")

book_bid_line, = ax_book.plot([], [], label="Best Bid", color="blue")
book_ask_line, = ax_book.plot([], [], label="Best Ask", color="red")
my_bid_scatter = ax_book.scatter([], [], marker="^", s=60, label="My Bid", color="green")
my_ask_scatter = ax_book.scatter([], [], marker="v", s=60, label="My Ask", color="orange")
ax_book.set_title("Order Book + My Quotes")
ax_book.set_xlabel("Tick")
ax_book.set_ylabel("Price")
ax_book.legend()

listener = data_listener()

def update(_frame):
    try:
        msg = next(listener)
    except StopIteration:
        return

    tick_series.append(msg["tick"])
    pnl_series.append(msg["pnl"])
    bid_series.append(msg["best_bid"])
    ask_series.append(msg["best_ask"])
    my_bid_series.append(msg["my_bid"])
    my_ask_series.append(msg["my_ask"])

    # Update PnL plot
    pnl_line.set_data(tick_series, pnl_series)
    ax_pnl.set_xlim(0, max(50, tick_series[-1]))
    ax_pnl.set_ylim(min(pnl_series) - 1, max(pnl_series) + 1)

    # Update Order Book plot
    book_bid_line.set_data(tick_series, bid_series)
    book_ask_line.set_data(tick_series, ask_series)
    my_bid_scatter.set_offsets(list(zip(tick_series, my_bid_series)))
    my_ask_scatter.set_offsets(list(zip(tick_series, my_ask_series)))

    ax_book.set_xlim(0, max(50, tick_series[-1]))
    ymin = min(filter(None, bid_series + my_bid_series)) - 0.1
    ymax = max(filter(None, ask_series + my_ask_series)) + 0.1
    ax_book.set_ylim(ymin, ymax)

    return (pnl_line, book_bid_line, book_ask_line, my_bid_scatter, my_ask_scatter)

ani = animation.FuncAnimation(fig, update, interval=100, blit=False)
plt.show()

