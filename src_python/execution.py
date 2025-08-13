class ExecutionEngine:
    def __init__(self):
        self.orders = []

    def send_order(self, order):
        self.orders.append(order)
        return {"status": "ack", "order": order}

    def cancel_order(self, order_id):
        self.orders = [o for o in self.orders if o["id"] != order_id]
        return {"status": "canceled", "id": order_id}

