from aioleakybucket import base, consts, handler


def test_noburst():
    zone = base.Zone('2r_s', max_elements=1, rate=2)

    limit = base.Limit(zone, 0, nodelay=True)

    class Req:
        limit_set = False

    r = Req()

    ms = 1000

    for step in range(100):
        pair = handler(ms, r, [limit])

        assert pair[0] == consts.DECLINED

        ms += 500
        r.limit_set = False

    ms -= 1

    pair = handler(ms, r, [limit])

    assert pair[0] == consts.TOO_MANY
