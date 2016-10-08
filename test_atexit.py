from threading import Thread, current_thread

import atexit

def exit0(*args, **kwargs):
    print '** exit0', current_thread().getName(), args, kwargs

def exit1():
    print '** exit1', current_thread().getName()
    raise Exception, 'exit1'

def exit2():
    print '** exit2', current_thread().getName()

atexit.register(exit0, 1, 2, a=1)
atexit.register(exit1)
atexit.register(exit2)

@atexit.register
def exit3():
    print '** exit3', current_thread().getName()

if __name__ == "__main__":
    print '** main', current_thread().getName()
