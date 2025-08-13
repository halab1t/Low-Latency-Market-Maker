import statistics

class LatencyMetrics:
    def __init__(self):
        self.latencies = []

    def record(self, start_ns, end_ns):
        self.latencies.append(end_ns - start_ns)

    def summary(self):
        if not self.latencies:
            return {}
        return {
            "p50": statistics.median(self.latencies),
            "p95": sorted(self.latencies)[int(0.95 * len(self.latencies))],
            "max": max(self.latencies)
        }

