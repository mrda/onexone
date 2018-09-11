import functools


_debug = False


def trace(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print('TRACE: Calling {}() with {}, {}'
              .format(func.__name__, args, kwargs))
        original_result = func(*args, **kwargs)
        print('TRACE: {}() returned {}'.format(func.__name__, original_result))
        return original_result
    if _debug:
        return wrapper
    else:
        return func
