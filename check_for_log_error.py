#/usr/sbin/python3
import sys
import os

SMOKING_GUN = "Removed Ice UpdatingAuthenticator"
LOG_FILE = "/home/douglas/Playground/kairos/test.log"

def write_stdout(s):
    # only eventlistener protocol messages may be sent to stdout
    sys.stdout.write(s)
    sys.stdout.flush()

def write_stderr(s):
    sys.stderr.write(s)
    sys.stderr.flush()

def parse_error(line):
    return line

def error_in_line(line):
    if SMOKING_GUN in line:
        return True
    return False

def parse_log():
    last_error = ""

    log_file = ""
    try:
        log_file = os.environ['SVLOG']
    except KeyError as e:
        log_file = LOG_FILE
    
    try:
        with open(log_file, 'r') as log:
            for log_line in log.readlines():
                if error_in_line(log_line):
                    last_error = parse_error(line)
    except FileNotFoundError as e:
        write_stderr(f"Log file: {LOG_FILE} not found!")
    return last_error

def main():
    write_stderr("STARTED")

    # Initial value is blank, so if there is no error it won't be restarted
    last_error = ""

    while 1:
        # transition from ACKNOWLEDGED to READY
        write_stdout('READY\n')

        #######################
        # This just waits for supervisord to say "hey do your thing"
        # read header line
        line = sys.stdin.readline()

        # read event payload
        headers = dict([ x.split(':') for x in line.split() ])
        data = sys.stdin.read(int(headers['len']))
        # Ok let's do our thing
        ######################

        current_error = parse_log()
        if last_error != current_error:
            last_error = current_error
            write_stderr(f"FOUND BAD LOGLINE: {last_error}")

        # transition from READY to ACKNOWLEDGED
        write_stdout('RESULT 2\nOK')

if __name__ == '__main__':
    main()
