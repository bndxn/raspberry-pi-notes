# Use this to control collecting temperatures and saving them to a DB

import schedule
import time

def job():
    print("I'm working...")

schedule.every(5).seconds.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)


print('Hello')
