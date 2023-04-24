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
from datetime import datetime, timedelta



AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
REGION_NAME = os.getenv('AWS_DEFAULT_REGION')


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

    # def get_readings(self, timestamp_range):
    #   """
    #   When finished this function should be able to query the DDB table

    #   """
    #   try:
    #     response = self.table.query(KeyConditionExpression=Key('timestamp').between(timestamp_range[0], timestamp_range[1]))
    #   except ClientError as err:
    #     print(f'Error: {err}')       
    #   else:
    #       return response['Items']
    
    # def get_readings_alt(self, timestamp_range):
       
    #   key_condition_expression = 'timestamp BETWEEN :min_value AND :max_value'
    #   expression_attribute_values = {':min_value': {'S': str(timestamp_range[0])},':max_value': {'S': str(timestamp_range[1])}}

    #   # Execute the query
    #   response = self.table.query(KeyConditionExpression=key_condition_expression, ExpressionAttributeValues=expression_attribute_values)

    #   items = response['Items']
    #   for item in items:
    #         print(item)




readings = list[Temper]()
        

# def upload_data_DDB(reading):
#     print('Uploading to DDB')
#     upload = DDBReadings()
#     datetime = str(pd.Timestamp.now())
#     temperature = reading[0]
#     humidity = reading[1]
#     print(f'DDB upload: Datetime: {datetime}, temp: {temperature}, hum: {humidity}')
#     upload.add_reading(datetime, temperature, humidity)


# def temper_ddb():
#     # Create an instance of the class
#     temper = Temper()
#     # Call the instance objects
#     reading = temper.main()
#     # Do the 
#     upload_data_DDB(reading)



def query_data_DDB():
    print('Querying DDB')
    DDBReading = DDBReadings() # Creating this object to get the connection, should rename it
    
    # Define the date range to search for
    start_date = datetime(2023, 4, 20)
    end_date = datetime(2023, 4, 22)

    # Convert the start and end dates to strings in ISO format
    start_date_str = start_date.strftime('%Y-%m-%d %H:%M:%S')
    end_date_str = end_date.strftime('%Y-%m-%d %H:%M:%S')
 
    start_date_str = str(pd.Timestamp.now() - pd.Timedelta(days=1))
    end_date_str = str(pd.Timestamp.now())


    key_condition_expression = '#ts BETWEEN :min_value AND :max_value'
    expression_attribute_values = {':min_value': {'S': start_date_str},':max_value': {'S': end_date_str}}
    expression_attribute_names = {'#ts':'timestamp'}

    # Execute the query
#    response = DDBReading.table.query(
#       KeyConditionExpression=key_condition_expression, 
#       ExpressionAttributeValues=expression_attribute_values,
#       ExpressionAttributeNames=expression_attribute_names
#       )

    items = response['Items']
    df = pd.DataFrame(items)
    df['timestamp'] = pd.to_datetime(df['timestamp'].str['S'])
    print(df)


def query_data_by_temp():
    print('Querying DDB by temp')
    DDBReading = DDBReadings()
    
    filter_expression = 'CAST(temperature AS NUMBER) > :temperature_value'
    expression_attribute_values = {':temperature_value': {'N':'18'}

    response = DDBReading.table.scan(FilterExpression=filter_expression, ExpressionAttributeValues=expression_attribute_values)

    items = response['Items']
    for item in items:
     print(item)

if __name__ == '__main__':
   query_data_by_temp()
#  schedule.every(2).seconds.do(temper_ddb)

#while True:p
#      schedule.run_pending()
#      time.sleep(1)
