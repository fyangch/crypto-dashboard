import sys
import os
import psutil
import time
from datetime import datetime
import logging

from src.market_data import update_market_data


def check_parent_process() -> None:        
    """
    Exit if the parent process is not running anymore. 
    """
    if not psutil.pid_exists(os.getppid()):
        sys.exit()


def clean_up_files() -> None:
    """
    Keep CSV files with market data from the previous two updates
    and delete the remaining files.
    """
    # TODO
    raise NotImplementedError()


if __name__ == "__main__":
    # TODO: Set up logger with console and file handler. Print timestamps for each message.

    while True:
        check_parent_process()
        
        # update market data every 5 minutes
        if datetime.now().minute % 5 == 0:
            update_market_data()
            clean_up_files()
        
        time.sleep(15)
