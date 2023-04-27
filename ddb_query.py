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
    
    self.dynamodb = boto3.client('dynamodb', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name=REGION_NAME)

  def query_last_day_of_readings(self):
      # Define the table name
      table_name = 'pi-temperature-readings'

      day_ago = str(pd.Timestamp.now() - pd.Timedelta(days=1))

      scan_params = {
          'TableName': table_name,
          'FilterExpression': '#ts > :day_ago',
          'ExpressionAttributeNames': {'#ts': 'timestamp'},
          'ExpressionAttributeValues': {':day_ago': {'S': day_ago}}
      }

      response_ts = self.dynamodb.scan(**scan_params)

      print('Timestamp response: json_normalise')
      df = pd.json_normalize(response_ts['Items'])
      print(df)


if __name__ == '__main__':
   dynamoresource = DynamoResource()
   dynamoresource.query_last_day_of_readings()
   print('Done')

