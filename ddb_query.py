# Use this to query temperatures
#!/usr/bin/python3

# Source code; https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GettingStarted.Query.html
import os
import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
import pandas as pd
from datetime import datetime, timedelta

class DynamoResource():
  
  def __init__(self):
    """
    :param dyn_resource: A Boto3 DynamoDB resource.
    """
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    REGION_NAME = os.getenv('AWS_DEFAULT_REGION')

    # dyn_resource = boto3.resource('dynamodb', 
    #                               aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name=REGION_NAME)
    # self.table = dyn_resource.Table('pi-temperature-readings')
    self.dynamodb = boto3.client('dynamodb', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY region_name=REGION_NAME)


  def query_time_range(self):
    print('Querying DDB for time range')    
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

    #Execute the query
    response = dynamoresource.table.query(
      KeyConditionExpression=key_condition_expression, 
      ExpressionAttributeValues=expression_attribute_values,
      ExpressionAttributeNames=expression_attribute_names
      )

    items = response['Items']
    df = pd.DataFrame(items)
    df['timestamp'] = pd.to_datetime(df['timestamp'].str['S'])
    
    print(df)


  def query_data_by_temp(self):
      # Define the table name
      table_name = 'pi-temperature-readings'

      # Define the scan parameters
      scan_params = {
          'TableName': table_name,
          'FilterExpression': '#temp > :temp_val',
          'ExpressionAttributeNames': {'#temp': 'temperature'},
          'ExpressionAttributeValues': {':temp_val': {'S': '18'}}
      }

      day_ago = str(pd.Timestamp.now() - pd.Timedelta(days=1))

      scan_params_ts = {
          'TableName': table_name,
          'FilterExpression': '#ts > :day_ago',
          'ExpressionAttributeNames': {'#ts': 'timestamp'},
          'ExpressionAttributeValues': {':day_ago': {'S': day_ago}}
      }

      # Scan the table with the defined parameters, references the instance of the class
      response = self.dynamodb.scan(**scan_params)
      response_ts = self.dynamodb.scan(**scan_params_ts)

      # Print the items where the temperature is above 18
      print('Temp response:')
      for item in response['Items']:
        print(item)

      print('Timestamp response:')
      for item in response_ts['Items']:
        print(item)


if __name__ == '__main__':
   #dynamoresource = DynamoResource()
   query_data_by_temp()
   print('Done')

