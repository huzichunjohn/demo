#!/usr/bin/env python

import subprocess
from threading import Timer

def kill(process):
    print "kill"
    process.kill()
    
#kill = lambda process: process.kill()

if __name__ == "__main__":
    cmd1 = ["sleep", "30"]
    cmd2 = ["ls", "-al"]

    p1 = subprocess.Popen(cmd1, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    timer1 = Timer(5, kill, [p1])

    try:
        timer1.start()
        stdout, stderr = p1.communicate()
        print stdout
        print stderr
    finally:
        timer1.cancel() 
  
    p2 = subprocess.Popen(cmd2, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    timer2 = Timer(5, kill, [p2])

    try:
        timer2.start()
        stdout, stderr = p2.communicate()
        print stdout
        print stderr
    finally:
        timer2.cancel()
