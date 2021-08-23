#!/usr/sbin/python
import time
import sys

def main():
    while(1):
        sys.stderr.write(".")
        sys.stderr.flush()
        time.sleep(60)

if __name__ == '__main__':
    main()
