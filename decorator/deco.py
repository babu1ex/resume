from functools import wraps


def parametr_deco(retry_count, expected_exceptions=()):
    def retry_deco(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            last_exception = None
            for attempt in range(1, retry_count + 1):
                try:
                    result = func(*args, **kwargs)
                    log = (
                        f"run {func.__name__} with positional args = {args}, "
                        f"keyword kwargs = {kwargs}, attempt = {attempt}, "
                        f"result = {result}"
                    )
                    print(log)
                    return result
                except expected_exceptions as er:
                    exception_name = type(er).__name__
                    log = (
                        f"run {func.__name__} with positional args = {args}, "
                        f"keyword kwargs = {kwargs}, attempt = {attempt}, "
                        f"exception = {exception_name} # нет перезапуска"
                    )
                    print(log)
                    raise
                except Exception as er:  # pylint: disable=broad-exception-caught
                    exception_name = type(er).__name__
                    log = (
                        f"run {func.__name__} with positional args = {args}, "
                        f"keyword kwargs = {kwargs}, attempt = {attempt}, "
                        f"exception = {exception_name}"
                    )
                    print(log)
                    last_exception = er
            if last_exception:
                raise last_exception
            return None
        return wrapper
    return retry_deco
