def set_clocks():
    def decorator(func):
        setattr(func, 'clocks', True)
        return func

    return decorator
