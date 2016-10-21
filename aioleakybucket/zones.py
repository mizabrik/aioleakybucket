from .base import Zone

_kb = 1024
_mb = _kb ** 2
_per_kb = 10

z2r_m = Zone('2r_m', max_elements=16 * _mb * _per_kb, rate=2/60)
z5r_m = Zone('5r_m', max_elements=64 * _mb * _per_kb, rate=5/60)
z10r_m = Zone('10r_m', max_elements=64 * _mb * _per_kb, rate=10/60)
z20r_m = Zone('20r_m', max_elements=64 * _mb * _per_kb, rate=20/60)
z30r_m = Zone('30r_m', max_elements=64 * _mb * _per_kb, rate=30/60)

z32r_s = Zone('32r_s', max_elements=64 * _mb * _per_kb, rate=32)
z2r_s = Zone('2r_s', max_elements=64 * _mb * _per_kb, rate=2)
z4r_s = Zone('4r_s', max_elements=64 * _mb * _per_kb, rate=4)


POPULAR = {
    '2r/m': z2r_m, '2r_m': z2r_m,
    '5r/m': z5r_m, '5r_m': z5r_m,
    '10r/m': z10r_m, '10r_m': z10r_m,
    '20r/m': z20r_m, '20r_m': z20r_m,
    '30r/m': z30r_m, '30r_m': z30r_m,
    '32r/s': z32r_s, '32r_s': z32r_s,
    '2r/s': z2r_s, '2r_s': z2r_s,
    '4r/s': z4r_s, '4r_s': z4r_s,
}
