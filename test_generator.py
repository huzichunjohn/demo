import time
import dis

def abc(seq):
    print "start abc"
    lst = list(seq)
    for i in lst:
        print lst
        print "before"
        value = yield i
        if value is not None:
            lst.append(value)
        print "end"
    print "end abc"

print dis.dis(abc)

r = abc([1, 2, 3])
print r.send(None)
time.sleep(2)

print r.send(None)
time.sleep(2)

print r.send(None)
time.sleep(2)

print r.send(4)
time.sleep(2)

print r.send(5)
time.sleep(2)
