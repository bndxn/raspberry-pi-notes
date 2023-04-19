# Use this to control collecting temperatures and saving them to a DB
#!/usr/bin/python3

import schedule
import time
from temper import Temper
import numpy as np
import pandas as pd
import boto3
from collect_and_upload_ddb import DDBReadings, add_reading


# copied this from pi_to_aws.py, not sure what it does
readings = list[Temper]()

def upload_data(readings):
    print('Uploading to S3')
    s3 = boto3.resource('s3')
    pd.DataFrame(readings).to_csv("readings_for_upload.csv")
    s3.Bucket('pi-temperature-readings').upload_file(
        Filename='readings_for_upload.csv', Key='test2.csv')
    print('Upload to S3 complete')
    
#    s3.Bucket('bucket-swiykr').upload_file(
#	Filename='readings_for_upload.csv', Key='test2.csv')
#    print('Upload to Lightsail S3 complete')



def temper():
    # Create an instance of the class
    temper = Temper()
    # Call the instance objects
    reading = temper.main()
    reading.append(pd.Timestamp.now())
    readings.append(reading)
    print(reading, len(readings))
    if len(readings) > 10:
        upload_data(readings)
        readings.clear()
        
schedule.every(0.1).seconds.do(temper)

while True:
    schedule.run_pending()
    time.sleep(1)




upload_data(readings)

# if __name__ == "__main__":
#    while True:
#        reading = 
