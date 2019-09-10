from time import time


def timeit(func, *args, **kwargs):
    """
    Times the execution of a function, and prints the runtime. For example:

    def foo(bar: int) -> int:
        return bar

    bar = timeit(foo, 1) # 1
    """
    t = time()
    res = func(*args, **kwargs)
    delta = time() - t
    print("{} took {:.2f} seconds to execute".format(func.__name__, delta))
    return res


def timeit_multiple(func, iters, *args, **kwargs):
    """
    Runs func iters times, and prints the total runtime.
    Note that if func is side-effecting, the effect will be performed
    multiple times.
    :return the last value returned by func
    """
    t = time()
    for i in range(iters):
        res = func(*args, **kwargs)
    delta = time() - t
    print("{} took {:.2f} seconds to execute".format(func.__name__, delta))
    return res
