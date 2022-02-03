import time 
import logging
from functools import wraps


def func_time(func):
    @wraps(func)
    def _time_it(*args, **kwargs):
        start_time = time.perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            end_time = time.perf_counter() - start_time
            logging.info(
                f"Total execution time {func.__name__}: {end_time if end_time > 0 else 0: .2f} s"
            )

    return _time_it
