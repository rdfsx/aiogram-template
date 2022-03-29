def lock_up():
    def decorator(func):
        setattr(func, "lock", True)
        return func

    return decorator
