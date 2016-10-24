class Delayer:

    def __init__(self, incrementor):
        self.incrementor = incrementor

    async def __call__(self, delay, *, loop=None):
        self.incrementor.current += delay * 1000
