# Use this to control collecting temperatures and saving them to a DB
#!/usr/bin/python

import schedule
import time
from temper import Temper


def temper():
    # Create an instance of the class
    temper = Temper()
    # Call the instance objects
    temper.main('--json')

schedule.every(0.1).seconds.do(temper)

while True:
    schedule.run_pending()
    time.sleep(1)

