# This file should provide the DDB querying tools for application.py, but should also work as a standalone

#!/usr/bin/python3
import os
import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
import pandas as pd

class DynamoResource():
  
  def __init__(self):
    
    self.dynamodb = boto3.client('dynamodb', 
                                 aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'), 
                                 aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'), 
                                 region_name=os.getenv('AWS_DEFAULT_REGION'))

  def query(self, since_timestamp=None):
      
      table_name = 'pi-temperature-readings'

      if since_timestamp == None:
        start_date =  str(pd.Timestamp('2023-04-28'))
      else:
        start_date = since_timestamp

      scan_params = {
          'TableName': table_name,
          'FilterExpression': '#ts > :start_date',
          'ExpressionAttributeNames': {'#ts': 'timestamp'},
          'ExpressionAttributeValues': {':start_date': {'S': start_date}}
      }

      response_ts = self.dynamodb.scan(**scan_params)

      print('Timestamp response: json_normalise')
      df = pd.json_normalize(response_ts['Items'])
      df.sort_values(by='timestamp.S',inplace=True)

      df.rename(columns={'humidity.S': 'humidity',
                   'temperature.S':'temperature',
                   'timestamp.S':'timestamp'},inplace=True)
   
      df[['humidity', 'temperature']] = df[['humidity', 'temperature']].apply(pd.to_numeric)      

      return df


if __name__ == '__main__':
   dynamoresource = DynamoResource()
   dynamoresource.query()
   print('Done')

