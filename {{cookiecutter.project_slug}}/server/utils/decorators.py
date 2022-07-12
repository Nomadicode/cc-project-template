def auth(*args, **kwargs):
    def inner(func):
        print(func)
        print(**kwargs)
        return func
    return inner


def get(*args, **kwargs):
    def inner(func):
        print(func)
        print(**kwargs)
        return func
    return inner

def create(*args, **kwargs):
    def inner(func):
        print(func)
        print(**kwargs)
        return func
    return inner

def update(*args, **kwargs):
    def inner(func):
        print(func)
        print(**kwargs)
        return func
    return inner

def delete(*args, **kwargs):
    def inner(func):
        print(func)
        print(**kwargs)
        return func
    return inner