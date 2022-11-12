import functools
import time

def memoize(function):
    function._cache = {}
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        # save args 
        prev_args = (args, tuple(kwargs.items()))
        if prev_args in function._cache.keys():
            return function._cache[prev_args]
        else:
            function._cache.update({prev_args: function(*args, **kwargs)})
            return function(*args, **kwargs)
    return wrapper

# example
@memoize
def long_operation(x, y):
    time.sleep(3)   # Or some other suitable long expression.
    return x + y

# test
# first call
print('Making uncached call...')
start_time = time.time()
long_operation(1, 2)
print("--- %s seconds ---" % (time.time() - start_time))

# cached call 
print('Making cached call...')
start_time = time.time()
long_operation(1, 2)
print("--- %s seconds ---" % (time.time() - start_time))