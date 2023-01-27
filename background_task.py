import time
from datetime import datetime
import logging

from src.market_data import update_market_data
from src.utils import check_parent_process, clean_up_files


if __name__ == "__main__":
    # TODO: Set up logger with console and file handler. Print timestamps for each message.

    update_market_data()
    
    while True:
        check_parent_process()
        
        # update market data every 5 minutes
        if datetime.now().minute % 5 == 0:
            update_market_data()
            clean_up_files()
        
        time.sleep(15)
