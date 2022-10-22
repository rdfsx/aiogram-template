def rate_limit(limit: float, key: str = None):
    def decorator(func):
        setattr(func, "throttling_rate", limit)
        if key:
            setattr(func, "throttling_key", key)
        return func

    return decorator
