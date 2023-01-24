import sys
import os
import psutil
import time


def check_parent_process():        
    """
    Exit if the parent process is not running anymore. 
    """
    if not psutil.pid_exists(os.getppid()):
        sys.exit()


if __name__ == '__main__':
    while True:
        time.sleep(60)
        check_parent_process()

        # TODO: Update market data
