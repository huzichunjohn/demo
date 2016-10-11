import csv
import re

PATTERN = re.compile(r'(\[|\])')

def read_from_file():
    for line in open('/tmp/access.log'):
        yield PATTERN.sub('"', line)

if __name__ == "__main__":
    reader = csv.DictReader(read_from_file(), fieldnames=["remote_host", "remote_logname", "remote_user", "time_stamp", "request_line", "status", "response_size", "referer_url", "user_agent"], delimiter=' ', quotechar='"')
    for line in reader:
        print line
