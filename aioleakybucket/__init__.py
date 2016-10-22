import asyncio
import collections
import logging
import timeit

from . import consts, bucket


logger = logging.getLogger(__name__)


def handler(simtime_msec, req, limits):

    if req.limit_set:
        return consts.DECLINED, None

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
        return rc, None
    r.limit_set = True

    if (busy == rc) or (error == rc):
        if busy == rc:
            logger.info(
                'limiting calls, excess: %d.%03d by zone \"%s\"',
                excess / 1000, excess % 1000, limit.zone,
            )

        while n > 0:
            n -= 1
            state = limits[n].zone.state

            if state is not None:
                state.count -= 1

            limits[n].zone.state = None

        return consts.TOO_MANY, None

    if consts.AGAIN == rc:
        excess = 0

    delay, excess, limit = bucket.account(
        simtime_msec, limits, n, excess, limit,
    )

    if not delay:
        return consts.DECLINED, None

    logger.debug(
        'delaying request, excess: %d.%03d by zone \"%s\"',
        excess / 1000, excess % 1000, limit.zone,
    )

    return consts.AGAIN, delay


def limit_call(zone, burst=None, nodelay=False,
               get_key=base.default_hash,
               timer=lambda: timeit.default_timer() * 1000,
               callback_limit=lambda *args, **kwargs: None,
               callback_error=lambda *args, **kwargs: None,
               loop=None):

    limit = base.Limit(zone, burst, nodelay, get_key)

    def wrapper(fn):

        if hasattr(fn, 'limits'):
            fn.limits.append(limit)
            return fn

        async def wrap(*args, **kwargs):
            rc, delay = handler(timer(), (args, kwargs), limits)

            if consts.ERROR == rc:
                return callback_error(*args, **kwargs)

            if consts.TOO_MANY == rc:
                return callback_limit(*args, **kwargs)

            if consts.AGAIN == rc:
                await asyncio.sleep(delay / 1000, loop=loop)
            else:
                assert consts.DECLINED == rc

            result = fn(*args, **kwargs)

            if isinstance(result, collections.Awaitable):
                return await result
            else:
                return result

        wrap.limits = [limit]

        return wrap

    return wrapper
