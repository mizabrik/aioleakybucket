import sys
import time


if sys.version_info >= (3, 7):
    def default_timer():
        return time.monotonic_ns() // 1000000
else:
    def default_timer():
        return int(time.monotonic() * 1000)


class Incrementer:
    def __init__(self, start=0, step=100):
        self.current = start
        self.step = step
        self.calls = 0

    def __call__(self):
        current = self.current
        self.current += self.step
        self.calls += 1

        return current
