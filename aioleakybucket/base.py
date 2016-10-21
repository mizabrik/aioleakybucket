import heapdict

from .utils import frozendict


def default_hash(*args, **kwargs):
    return hash((tuple(args), frozendict.FrozenDict(kwargs)))


class Zone(object):
    __slots__ = ('states', 'rate', 'state', 'name', 'max_elements')

    def __str__(self):
        return self.name

    def __repr__(self):
        # TODO: output rate with best /s
        return '<Zone %s, rate=%s>' % (self.name, self.rate)

    def __init__(self, name, rate, max_elements=1000*1000):
        self.name = name

        # TODO:parse /s /m and so on
        self.rate = rate * 1000
        self.state = None
        self.states = heapdict.heapdict()
        self.max_elements = max_elements


class Limit(object):
    __slots__ = ('zone', 'burst', 'nodelay', 'get_key')

    def __init__(self, zone, burst, nodelay=False, get_key=default_hash):
        self.zone = zone
        self.burst = burst * 1000
        self.nodelay = nodelay
        self.get_key = get_key

    def __repr__(self):
        return '<Limit burst=%s nodelay=%s zone=%s>' % (
            self.burst, self.nodelay, self.zone,
        )


class State(object):
    __slots__ = ('excess', 'count', 'last')

    def __init__(self, excess, count=0, last=0):
        self.excess = excess
        self.count = count
        self.last = last

    def __repr__(self):
        return '<State excess=%s count=%s last=%s>' % (
            self.excess, self.count, self.last,
        )
