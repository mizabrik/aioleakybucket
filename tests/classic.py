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


def test_burst():
    zone = base.Zone('1r_s', max_elements=1, rate=1)
    limit = base.Limit(zone, 10, nodelay=True)


    class Req:
        limit_set = False

    r = Req()
    ms = 1000

    for step in range(100):
        pair = handler(ms, r, [limit])

        assert pair[0] == consts.DECLINED

        ms += 1000

        r.limit_set = False

    for step in range(10 + 2):
        pair = handler(ms, r, [limit])

        assert pair[0] == consts.DECLINED

        ms += 100

        r.limit_set = False

    ms -= 1

    pair = handler(ms, r, [limit])

    #assert list(limit.zone.states.values())[0][1].excess == 10000.0

    assert pair[0] == consts.TOO_MANY
