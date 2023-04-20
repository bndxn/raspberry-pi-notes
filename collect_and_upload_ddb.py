# Use this to control collecting temperatures and saving them to a DB
#!/usr/bin/python3


# Source article: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/example_dynamodb_PutItem_section.html

# Source code: https://github.com/awsdocs/aws-doc-sdk-examples/blob/main/python/example_code/dynamodb/GettingStarted/scenario_getting_started_movies.py#L151


import schedule
import time
from decimal import Decimal
from io import BytesIO
import json
import logging
import os
from pprint import pprint
import requests
from zipfile import ZipFile
import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
from temper import Temper
import pandas as pd


class DDBReadings():
  
    def __init__(self):
      """
      :param dyn_resource: A Boto3 DynamoDB resource.
      """
      self.session = boto3.Session(profile_name='default')
      self.dyn_resource = self.session.boto3.resource('dynamodb', region_name='eu-west-1')
      self.table_name = 'pi-temperature-readings'
      self.table = self.dyn_resource.Table('pi-temperature-readings')

    def add_reading(self, datetime, temperature, humidity):
      """
      Adds a temperature and humidity reading to the table. 
      
      :param datetime: the time the reading was taken
      :param temperature: temperature as measured by the probe
      :param humidity: humidity as measured by the probe
      """
      try: 
        self.table.put_item(
          Item={
            'datetime': datetime, 
            'temperature': temperature, 
            'humidity': humidity})
      except ClientError as err:
        print(err)
        # logger.error(
        #   "Couldn't add reading at % to table. Here's why: %s: %s",
        #   err.response['Error']['Code'], err.response['Error']['Message'])
     
    # Scanning for readings: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/example_dynamodb_Scan_section.html
    # Another source, simpler code: https://docs.aws.amazon.com/code-library/latest/ug/python_3_dynamodb_code_examples.html

    def get_readings(self, time_range):
      """
      When finished this function should be able to query the DDB table

      """

      try:
        response = self.table.query(KeyConditionExpression=Key('year').eq(year))
      except ClientError as err:
        print(f'Error: {err}')       
      else:
          return response['Items']
        


readings = list[Temper]()
        

def upload_data_DDB(reading):
    print('Uploading to DDB')
    upload = DDBReadings()
    datetime = str(pd.Timestamp.now())
    temperature = reading[0]
    humidity = reading[1]
    print(f'DDB upload: Datetime: {datetime}, temp: {temperature}, hum: {humidity}')
    upload.add_reading(datetime, temperature, humidity)


def temper_ddb():
    # Create an instance of the class
    temper = Temper()
    # Call the instance objects
    reading = temper.main()
    # Do the upload
    upload_data_DDB(reading)

if __name__ == '__main__':
  schedule.every(2).seconds.do(temper_ddb)

  while True:
      schedule.run_pending()
      time.sleep(1)
