# Use this to control collecting temperatures and saving them to a DB
#!/usr/bin/python

import schedule
import time
from temper import Temper
import numpy as np
import pandas as pd

# copied this from pi_to_aws.py, not sure what it does
readings = list[Temper]()

def temper():
    # Create an instance of the class
    temper = Temper()
    # Call the instance objects
    reading = temper.main()
    reading.append(pd.Timestamp.now())
    readings.append(reading)

schedule.every(0.1).seconds.do(temper)

i = 0
while i < 3:
    i += 1
    schedule.run_pending()
    time.sleep(1)

print(readings)

pd.DataFrame(readings).to_csv("readings.csv")

# np.savetxt("readings.csv", readings, delimiter = ',', fmt='%.3e')

# if __name__ == "__main__":
#    while True:
#        reading = 
