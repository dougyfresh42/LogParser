#!/usr/sbin/python
import time
import sys

def main(start_time):
    while(1):
        sys.stderr.write(f"{start_time}\n")
        sys.stderr.flush()
        time.sleep(60)

if __name__ == '__main__':
    sys.stderr.write("Started!\n")
    sys.stderr.flush()
    main(time.time())
