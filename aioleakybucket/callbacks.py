import logging

logger = logging.getLogger(__name__)


class LimitCallError(RuntimeError):
    pass


def cb_ignore(*args, **kwargs):
    return


def cb_raise(*args, **kwargs):
    raise LimitCallError(
        'Error limiting calls params(*%r, **%r)' % (args, kwargs),
    )


def cb_log(*args, **kwargs):
    logger.debug('Processing limits for call with params(*r, **%r)',
                 args, kwargs)
