# Use this to query temperatures
#!/usr/bin/python3

# Source code; https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GettingStarted.Query.html
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


AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
REGION_NAME = os.getenv('AWS_DEFAULT_REGION')

#print(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, REGION_NAME)

class DDBReadings():
  
    def __init__(self):
      """
      :param dyn_resource: A Boto3 DynamoDB resource.
      """
      AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
      AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
      REGION_NAME = os.getenv('AWS_DEFAULT_REGION')

      dyn_resource = boto3.resource('dynamodb', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name='us-east-1')
      self.table = dyn_resource.Table('pi-temperature-readings')

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
            'timestamp': datetime, 
            'temperature': temperature, 
            'humidity': humidity})
      except ClientError as err:
        print(err)
        # logger.error(
        #   "Couldn't add reading at % to table. Here's why: %s: %s",
        #   err.response['Error']['Code'], err.response['Error']['Message'])
     
    # Scanning for readings: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/example_dynamodb_Scan_section.html
    # Another source, simpler code: https://docs.aws.amazon.com/code-library/latest/ug/python_3_dynamodb_code_examples.html

    def get_readings(self, timestamp_range):
      """
      When finished this function should be able to query the DDB table

      """
      try:
        response = self.table.query(KeyConditionExpression=Key('timestamp').between(timestamp_range[0], timestamp_range[1]))
      except ClientError as err:
        print(f'Error: {err}')       
      else:
          return response['Items']
    
    def get_readings_alt(self, timestamp_range):
       
      key_condition_expression = 'timestamp BETWEEN :min_value AND :max_value'
      expression_attribute_values = {':min_value': {'N': str(timestamp_range[0])},':max_value': {'N': str(timestamp_range[1])}}

      # Execute the query
      response = self.table.query(KeyConditionExpression=key_condition_expression,
      ExpressionAttributeValues=expression_attribute_values)

      items = response['Items']
      for item in items:
            print(item)


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
    # Do the 
    upload_data_DDB(reading)



def query_data_DDB():
    print('Querying DDB')
    query = DDBReadings() # Creating this object to get the connection, should rename it
    now =  str(pd.Timestamp.now())
    day_ago =  str(pd.Timestamp.now() - pd.Timedelta(days=1))
    timestamp_range = [day_ago, now]    
    query.get_readings_alt(timestamp_range)

if __name__ == '__main__':
   query_data_DDB()
#  schedule.every(2).seconds.do(temper_ddb)

#while True:
#      schedule.run_pending()
#      time.sleep(1)
