# Use this to query temperatures
#!/usr/bin/python3

# Source code; https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GettingStarted.Query.html
import os
import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
import pandas as pd
from datetime import datetime, timedelta

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
REGION_NAME = os.getenv('AWS_DEFAULT_REGION')


class DynamoResource():
  
  def __init__(self):
    """
    :param dyn_resource: A Boto3 DynamoDB resource.
    """
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    REGION_NAME = os.getenv('AWS_DEFAULT_REGION')

    dyn_resource = boto3.resource('dynamodb', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name='us-east-1')
    self.table = dyn_resource.Table('pi-temperature-readings')


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
    print('Querying DDB for temp')
    
    filter_expression = 'temperature > :temperature_value'
    expression_attribute_values = {':temperature_value': {'N':'18'}}

    response = dynamoresource.table.scan(FilterExpression=filter_expression, ExpressionAttributeValues=expression_attribute_values)

    items = response['Items']
    for item in items:
     print(item)

if __name__ == '__main__':
   dynamoresource = DynamoResource()
   try:
     dynamoresource.query_data_by_temp()
   except:
     dynamoresource.query_time_range()
   finally:
     print('Done')

