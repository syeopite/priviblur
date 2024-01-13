"""A simple counter to track how many requests experienced a PoolTimeout

Due to an upstream problem with httpx, the connection pool can become poisoned
with broken connections that'd always raise a PoolTimeout. Once the entire pool
becomes poisoned, all requests will fail.

By tracking the amount of PoolTimeouts (with frequent resets), we can detect
when a pool becomes poisoned and to create a new pool to replace it

For more information see https://github.com/syeopite/priviblur/issues/4
"""

class PoolTimeoutTracker:
    """Wraps a dictionary counting amount and origin of PoolTimeouts

    tracker = PoolTimeoutTracker()
    tracker.increment("someorigin")        # Increments both total and successful request count
    tracker.increment_total("someorigin")  # Increments only the total request count (failure)
    """
    def __init__(self):
        self.counter = {}

    def increment_total(self, origin):
        """Increments the total amount of requests in the pool"""
        if self.counter.get(origin):
            self.counter[origin]["total"] += 1
        else:
            self.counter[origin] = {"total": 1, "success": 0,}

    def increment(self, origin):
        """Increments the total and successful request count in the pool"""
        if self.counter.get(origin):
            self.counter[origin]["total"] += 1
            self.counter[origin]["success"] += 1
        else:
            self.counter[origin] = {"total": 1, "success": 1}
