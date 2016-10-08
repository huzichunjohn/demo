import sys

def trace_func(frame, event, args):
    if "a" not in frame.f_locals:
        return 

    value = frame.f_locals["a"]
    if value % 2 == 0:
        value += 1
        frame.f_locals["a"] = value

def print_odd(a):
    print a

if __name__ == "__main__":
    sys.settrace(trace_func)
    for i in range(0, 6):
        print_odd(i)
