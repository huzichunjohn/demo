#from greenlet import greenlet
import time
import greenlet

def test1():
    print("start test1")
    print(12)
    gr2.switch()
    print(34)
    print("end test1")

def test2():
    print("start test2")
    print(56)
    gr1.switch()
    print(78)
    print("end test2")

def test3(x, y):
    print("start test3")
    z = gr2.switch(x+y)
    print(z)
    print("end test3")

def test4(u):
    print("start test4")
    print(u)
    gr1.switch(43)
    print("end test4")

def foo(n):
    print("start foo")
    main.switch(n+1)
    print("end foo")

def bar(n):
    print("start bar")
    foo(n)
    print("end bar")
    return 'hello'

if __name__ == "__main__":
#    gr1 = greenlet(test3)
#    gr2 = greenlet(test4)
#    print("before")
#    gr1.switch("hello", "world") 
#    print("after")
    main = greenlet.getcurrent()
    g1 = greenlet.greenlet(bar)
    print(12)
    print(g1.switch(42))
    time.sleep(2)
    print(34)
    print(g1.switch())
    time.sleep(2)
    print(56)
    print(g1.dead)
    print(78)
