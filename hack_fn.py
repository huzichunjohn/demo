import sys

def trace_func(frame, event, args):
    print "#" * 10, "start trace_func", "#" * 10
    if "a" not in frame.f_locals:
        return 

    value = frame.f_locals["a"]
    print value
    if value % 2 == 0:
        value += 1
        print value
        frame.f_locals["a"] = value
    print "#" * 10, "end trace_func", "#" * 10

def print_odd(a):
    print "#" * 10, "start print_odd", "#" * 10
    print a
    print "#" * 10, "end print_odd", "#" * 10

if __name__ == "__main__":
    sys.settrace(trace_func)
    for i in range(0, 6):
        print_odd(i)
