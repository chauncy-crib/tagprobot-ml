from time import time


def timeit(func, *args, **kwargs):
    t = time()
    res = func(*args, **kwargs)
    delta = time() - t
    print("{} took {:.2f} seconds to execute".format(func.__name__, delta))
    return res


def timeit_multiple(func, iters, *args, **kwargs):
    t = time()
    for i in range(iters):
        res = func(*args, **kwargs)
    delta = time() - t
    print("{} took {:.3f} seconds to execute".format(func.__name__, delta))
    return res
