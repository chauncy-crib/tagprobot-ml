from time import time

def timeit(func, *args, **kwargs):
    t = time()
    func(*args, **kwargs)
    delta = time() - t
    print("{} took {:.2f} seconds to execute".format(func.__name__, delta))
