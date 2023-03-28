# Use this to control collecting temperatures and saving them to a DB

import schedule
import time
import temper


def job():
    print("I'm working...")

schedule.every(0.1).seconds.do(job)
schedule.every(0.1).seconds.do(temper)

while True:
    schedule.run_pending()
    time.sleep(1)


