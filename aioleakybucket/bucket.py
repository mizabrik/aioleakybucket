from . import base, consts


def account(ts, limits, n, excess, limit):
    excess_ret = excess

    if excess == 0 or limit.nodelay:
        max_delay = 0
    else:
        max_delay = excess * 1000 / limit.zone.rate;

    while n > 0:
        n -= 1
        zone = limits[n].zone
        state = zone.state

        if state is None:
            continue

        ms = ts - state.last
        excess = state.excess - zone.rate * abs(ms) / 1000 + 1000

        if excess < 0:
            excess = 0

        state.last = ts
        state.excess = excess
        state.count -= 1

        zone.state = None

        if limits[n].nodelay:
            continue

        delay = excess * 1000 / zone.rate

        if delay > max_delay:
            max_delay = delay
            excess_ret = excess
            limit = limits[n]

    return max_delay, excess_ret, limit


def lookup(ts, limit, key, excess, account):
    pair = limit.zone.states.get(key)

    if pair is not None:
        last, state = pair

        limit.zone.states[key] = (-ts, state)

        ms = ts - state.last

        excess = state.excess - limit.zone.rate * abs(ms) / 1000 + 1000

        if excess < 0:
            excess = 0

        if excess > limit.burst:
            return excess, consts.BUSY

        if account:
            state.excess = excess
            state.last = ts
            return excess, consts.OK

        state.count += 1
        limit.zone.state = state
        return excess, consts.AGAIN

    excess = 0

    # Free up to two expired nodes
    if limit.zone.expire(ts):
        limit.zone.expire(ts)

    # Zone max_elements must not be exceeded
    if len(limit.zone.states) >= limit.zone.max_elements:
        if not limit.zone.expire(ts, True):
            return excess, consts.ERROR

    state = base.State(excess)

    if account:
        state.count = 0
        state.last = ts
        limit.zone.states[key] = (-state.last, state)
        return excess, consts.OK

    state.count = 1
    state.last = 0
    limit.zone.states[key] = (-state.last, state)
    limit.zone.state = state

    return excess, consts.AGAIN
