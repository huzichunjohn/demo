#from collections import namedtuple
#Point = namedtuple('Point', ['x', 'y'])
#
#def monitor(self, item):
#    print "** accessing :" + item
#    return super(Point, self).__getattribute__(item)
#
#Point.__getattribute__ = monitor
#
#p = Point(x=1, y=2)
#print p.x
#print p.y
#
#def handle_non_exist(self, item):
#    print "** handling :" + item
#    return str(item)
#
#Point.__getattr__ = handle_non_exist
#
#print p.z

class IntegerProperty(object):
    def __init__(self, mi=None, mx=None):
        self.min = mi
        self.max = mx

    def __get__(self, obj, objtype):
        return self.val

    def __set__(self, obj, val):
        if (self.min is None or self.min <= val) and (self.max is None or val <= self.max):
            self.val = val
        else:
            raise ValueError("value is out of range")

class People(object):
    age = IntegerProperty(1, 130)
    height = IntegerProperty(1, 230)
    def __init__(self, age, height):
        self.age = age
        self.height = height

p = People(age=1, height=200)
print p.age

p.age = 10
print p.age

#p.age = 0
#p = People(age=-1, height=200)
#del p.age

class Call(object):
    def __mul__(self, other):
        print other
        return lambda a: a * other

    def __radd__(self, other):
        print other
        return lambda a: a + other

_ = Call()

print map(_ * 2, xrange(4))
print map(10 + _, xrange(4))


class Task(object):
    def __init__(self, name):
        self.name = name
        self.post_tasks = []

    def __rshift__(self, task):
        print "start", self.name
        print self.post_tasks
        self.post_tasks.append(task)
        print self.post_tasks
        print "end", self.name
        return task

    def __str__(self):
        return self.name

t1, t2, t3, t4, t5, t6, t7 = (Task('t' + str(x)) for x in range(1, 8))
t1 >> t2 >> t3 >> t4
t2 >> t5 >> t6
t1 >> t7

class Dag(object):
    @staticmethod
    def draw_task(task, level):
        print "  " * (level + 1) + " + " + str(task)

    @staticmethod
    def draw_dag(task, level=0):
        Dag.draw_task(task, level)
        for n in task.post_tasks:
            Dag.draw_dag(n, level+1)

Dag.draw_dag(t1)

import wrapt, time, threading, inspect, collections
from threading import Thread

def logger(prefix='*'):
    @wrapt.decorator
    def _logger(fn, instance, args, kwargs):
        print '{} Enter {}'.format(prefix, fn.func_name)
        ret = fn(*args, **kwargs)
        print '{} Exit "{}"'.format(prefix, fn.func_name)
        return ret
    return _logger

@wrapt.decorator
def timer(fn, instance, args, kwargs):
    t1 = time.time()
    ret = fn(*args, **kwargs)
    print "* Time consumed: {} seconds".format(time.time() - t1)
    return ret

@wrapt.decorator
def ignore_error(fn, instance, args, kwargs):
    try:
        return fn(*args, **kwargs)
    except Exception as e:
        print "# Skip errors: {}".format(e)

@wrapt.decorator
def dummy(fn, instance, args, kwargs):
    return "Do nothing"

#@timer
#@logger("+")
@dummy
@ignore_error
def do_job():
    print "Hello Pycon 2016 China!"
    raise ValueError("invalid")

print do_job()

@wrapt.decorator
def check_auth(fn, instance, args, kwargs):
    if getattr(instance, 'need_login', False) and not getattr(instance, 'session_key', ''):
        print "*** Permission Denied: {}".format(type(instance))
        return
    return fn(*args, **kwargs)

class HomePage(object):
    need_login = False

    @check_auth
    def show(self):
        print "** This is Home Page."

class AdminPage(object):
    need_login = True
    session_key = ''

    @check_auth
    def show(self):
        print "** This is Admin Page."

p1 = HomePage()
p2 = AdminPage()
p1.show()
p2.show()

def synchronized(cls):
    lock = threading.RLock()

    @wrapt.decorator
    def _wrapper(fn, instace, args, kwargs):
        with lock:
            return fn(*args, **kwargs)

    for k, v in cls.__dict__.iteritems():
        if not k.startswith("__") and inspect.isfunction(v):
            print k, v
            setattr(cls, k, _wrapper(v))
    return cls

@synchronized
class Task(object):
    def __init__(self):
        self.data = "xxx"

    def run1(self):
        data = self.data
        time.sleep(0.5)
        self.data = data + "111"

    def run2(self):
        data = self.data
        time.sleep(0.5)
        self.data = data + "222"

    def run3(self):
        data = self.data
        time.sleep(0.5)
        self.data = data + "333"

from threading import Thread

t = Task()
ts = [Thread(target=lambda j: j.run1(), args=(t,)), Thread(target=lambda j: j.run2(), args=(t,)), Thread(target=lambda j: j.run3(), args=(t,))]

[s.start() for s in ts]
[s.join() for s in ts]

print "final data:", t.data
assert len(t.data) == 12, "t.data length should be 12 but is " + str(len(t.data))

class RegisterLeafClasses(type):
    def __init__(cls, name, bases, nmspc):
        #print repr(cls), name, bases, nmspc
        super(RegisterLeafClasses, cls).__init__(name, bases, nmspc)
        if not hasattr(cls, 'registry'):
            cls.registry = set()
        cls.registry.add(cls)
        print cls.registry
        cls.registry -= set(bases)
        print cls.registry

    def __str__(cls):
        print id(cls.registry), repr(cls)
        if cls in cls.registry:
            return cls.__name__
        return cls.__name__ + ": " + ", ".join([sc.__name__ for sc in cls.registry])

class Color(object):
    __metaclass__ = RegisterLeafClasses

class Blue(Color): pass
class Red(Color): pass
class Green(Color): pass
class Yellow(Color): pass
print(Color)
print(Blue)
print(Red)
print(Green)
print(Yellow)
class PhthaloBlue(Blue): pass
class CeruleanBlue(Blue): pass
print(Color)

class final(type):
    def __init__(cls, name, bases, namespace):
        print cls, name, bases, namespace
        super(final, cls).__init__(name, bases, namespace)
        for klass in bases:
            print klass, type(klass)
            if isinstance(klass, final):
                print "**debug** ", name, bases, namespace
                raise TypeError(str(klass.__name__) + " is final")

class A(object):
    pass

class B(A):
    __metaclass__ = final

#class C(B):
#    pass

class SynchronizedClass(type):
    #@classmethod
    #def __prepare__(name, bases, **kwds):
    #    print("__prepare__")
    #    return collections.OrderedDict()

    def __new__(metacls, name, bases, namespace, **kwds):
        print("__new__")
        ret = type.__new__(metacls, name, bases, dict(namespace))
        
        ret.lock = threading.RLock()
        @wrapt.decorator
        def _wrapper(fn, instance, args, kwargs):
            with ret.lock:
                return fn(*args, **kwargs)

        for k, v in namespace.iteritems():
            if not k.startswith("__") and inspect.isfunction(v):
                setattr(ret, k, _wrapper(v))
        return ret

class Task(object):
    __metaclass__ = SynchronizedClass

    def __init__(self):
        self.data = "xxx"

    def run1(self):
        data = self.data
        time.sleep(0.5)
        self.data = data + "111"

    def run2(self):
        data = self.data
        time.sleep(0.5)
        self.data = data + "222"

    def run3(self):
        data = self.data
        time.sleep(0.5)
        self.data = data + "333"

t = Task()
ts = [Thread(target=lambda j: j.run1(), args=(t,)), Thread(target=lambda j: j.run2(), args=(t,)), Thread(target=lambda j: j.run3(), args=(t,))]
[s.start() for s in ts]
[s.join() for s in ts]

print "final data:", t.data
assert len(t.data) == 12, "t.data length should be 12 but is " + str(len(t.data))

import sys, re

def getchunks(s):
    matches = list(re.finditer(r"\$\{(.*?)\}", s))

    if matches:
        pos = 0
        for match in matches:
            yield s[pos: match.start()]
            yield [match.group(1)]
            pos = match.end()
        yield s[pos:]

def interpolate(templateStr):
    result = ''
    for chunk in getchunks(templateStr):
        print repr(chunk)
        if isinstance(chunk, list):
            result += str(eval(chunk[0]))
        else:
            result += chunk
    return result

name = 'Guido van Rossum'
places = 'Amsterdam', 'LA', 'New York', 'DC', 'Chicago'

s = """My name is ${'Mr. ' + name + ', Esquire'}.
I have visited the following cities: ${', '.join(places)}.
"""
print interpolate(s)
