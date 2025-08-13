class RiskManager:
    def __init__(self, max_inventory=10):
        self.inventory = 0
        self.max_inventory = max_inventory

    def adjust_orders(self, orders):
        """Cancel or adjust orders if inventory is too high/low"""
        adjusted = []
        for o in orders:
            if o["side"] == "B" and self.inventory >= self.max_inventory:
                continue
            if o["side"] == "S" and self.inventory <= -self.max_inventory:
                continue
            adjusted.append(o)
        return adjusted

