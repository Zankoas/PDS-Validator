import time


def timed_function(function):
    def time_wrapper(*args, *kwargs):
        t0 = time.time()
        function(*args, *kwargs)
        t0 = time.time() - t0
        print("Time taken for equipment bonus script: " + (t0 * 1000).__str__() + " ms")
    return time_wrapper