
# This is a first test of downloading from S3, in future to be integrated with plotly and flask web generation
#!/usr/bin/python3


import numpy as np
import pandas as pd
import boto3

def download_most_recent_temp():
    print('Downloading from S3')
    s3 = boto3.resource('s3')
    s3.Bucket('pi-temperature-readings').download_file('test2.csv','local_copy_test2.csv')
    df = pd.read_csv('local_copy_test2.csv')
    print(df)

download_most_recent_temp()
