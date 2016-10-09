import time

class MyTimer(object):
    def __init__(self, tag='default'):
        self.tag = tag

    def __enter__(self):
        self.start = time.time()

    def __exit__(self, exc, val, trace):
        self.end = time.time()
        print '*** performance for "' + self.tag + '" ***'
        print "    {} seconds".format(self.end - self.start)
        return True

def test1(x, max):
    try:
        1/(max-x-1)
    except ZeroDivisionError as e:
        raise

def test2(x, max):
    1/(max-x-1)

with MyTimer("function call"):
    for x in range(10000):
        test1(x, 10000)

print "-" * 30

with MyTimer("function call with try block"):
    try:
        for x in range(10000):
            test2(x, 10000)
    except ZeroDivisionError as e:
        raise

