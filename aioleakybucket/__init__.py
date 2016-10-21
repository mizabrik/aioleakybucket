from . import consts, bucket


def handler(simtime_msec, req, limits):

    if req.limit_set:
        return consts.DECLINED

    excess = 0

    rc = consts.DECLINED

    for n, limit in enumerate(limits):
        key = limit.get_key(req)

        is_last = (n == len(limits) - 1)

        excess, rc = bucket.lookup(
                simtime_msec, limit, key,
                excess, account=is_last,
        )

        if consts.AGAIN != rc:
            break
    else:
        n += 1

    if consts.DECLINED == rc:
        return rc
    r.limit_set = True

    if (busy == rc) or (error == rc):
        if busy == rc:
            print(
                'limiting requests, excess: %d.%03d by zone \"%s\"' %
                (excess / 1000, excess % 1000, limit.zone)
            )

        while n > 0:
            n -= 1
            state = limits[n].zone.state

            if state is not None:
                state.count -= 1

            limits[n].zone.state = None

        return '429'

    if consts.AGAIN == rc:
        excess = 0

    delay, excess, limit = bucket.account(
            simtime_msec, limits, n, excess, limit,
    )

    if not delay:
        return consts.DECLINED

    print(
        'delaying request, excess: %d.%03d by zone \"%s\"' %
        (excess / 1000, excess % 1000, limit.zone)
    )

    return consts.AGAIN, delay
