# Leaky bucket implementation ported from nginx

## Set up limits

```
zone = Zone('zone_name', rate_limit)
limit1 = Limit(zone, burst, nodelay)
```

## Default zones


## Decorators

```
@limit_calls(zone, burst, nodelay)
def some_function():
    """Usage with non-awatables"""
    return 0


@limit_calls(zone, burst, nodelay)
async def some_other_function():
    """Usage with awatables"""
    return await asincio.sleep(1)
```

## Manual mode
