import math

def fill_probability(mid, price, side):
    """
    Probability that an order is filled.
    Closer to mid = higher chance; aggressive (crossing mid) = almost certain.
    """
    dist = abs(price - mid)
    decay_rate = 40.0
    if (side == "B" and price >= mid) or (side == "S" and price <= mid):
        return 0.95
    return math.exp(-decay_rate * dist)

def simulate_fills(orders, mid, cash, inventory):
    """
    Takes list of orders and updates cash/inventory if fills occur.
    Returns new cash, new inventory.
    """
    for o in orders:
        side = o["side"]
        price = o["price"]
        qty = o["qty"]

        if fill_probability(mid, price, side) > 0.5:
            if side == "B":
                cash -= price * qty
                inventory += qty
            else:
                cash += price * qty
                inventory -= qty

    return cash, inventory

def mark_to_market(cash, inventory, mid):
    """
    Marks portfolio to midprice to calculate current equity.
    """
    return cash + inventory * mid

