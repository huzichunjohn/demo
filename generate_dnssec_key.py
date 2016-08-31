#!/usr/bin/python

import subprocess
import os

def generate_dnssec_key(keyname="test"):
    p = subprocess.Popen(["dnssec-keygen", "-a", "hmac-md5", "-b", "128", "-n", "HOST", keyname], stdout=subprocess.PIPE, stderr=subprocess.
PIPE)
    returncode = p.wait()
    (stdout, stderr) = p.communicate()
    stdout = stdout.strip()

    if returncode != 0:
        return None
    else:
        if os.path.exists(stdout+".key"):
            with open(stdout+".key") as f:
                line = f.readline()
            result = line.split()[6]
            
            # delete the generated key file and private file.
            os.remove(stdout+".key")
            os.remove(stdout+".private")

            return result
        else:
            return None

if __name__ == "__main__":
    print generate_dnssec_key()
