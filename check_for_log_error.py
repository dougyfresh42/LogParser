#/usr/sbin/python3
import sys
import os
import subprocess

SMOKING_GUN = "Removed Ice UpdatingAuthenticator"
LOG_FILE = "/home/douglas/Playground/kairos/test.log"
RESTART_CMD = ["supervisorctl", "-c", "/home/douglas/Playground/kairos/supervisord.conf", "restart", "authenticator.py"]

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
                    last_error = parse_error(log_line)
    except FileNotFoundError as e:
        write_stderr(f"Log file: {LOG_FILE} not found!")
    return last_error

def restart_authenticator():
    write_stderr("Restarting...\n")
    # Direct STDOUT to /dev/null - supervisord is listening on stdout
    # TODO this shouldn't be a hard coded command
    subprocess.run(RESTART_CMD,
                    stdout=subprocess.DEVNULL);

def main():
    write_stderr("STARTED\n")

    # Initial value is blank, so if there is no error it won't be restarted
    last_error = ""

    # Don't do this if it's the initial run
    first_run = True

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

        # On the first run, don't worry about the log
        if first_run:
            last_error = current_error
            first_run = False

        # Check if current_error is not blank first, in the chance that the
        # log gets rotated and the offending line is gone
        if current_error and (last_error != current_error):
            last_error = current_error
            write_stderr(f"\nFOUND BAD LOGLINE: {last_error}")
            restart_authenticator()

        # transition from READY to ACKNOWLEDGED
        write_stdout('RESULT 2\nOK')

if __name__ == '__main__':
    main()
