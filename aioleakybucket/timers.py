import timeit


def default_timer():
    return timeit.default_timer() * 1000


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
