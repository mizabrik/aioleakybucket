def expire(ts, zone, n):
    while n < 3:

        if len(zone.states) == 0:
            return

        key, (_, state) = zone.states.peekitem()

        if state.count:
            return

        if n != 0:
            n += 1

            ms = abs(ts - state.last)

            if ms < 60000:
                return

            excess = state.excess - zone.rate * ms / 1000

            if excess > 0:
                return
        else:
            n += 1

        del zone.states[key]


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
