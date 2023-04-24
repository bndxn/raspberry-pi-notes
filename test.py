#!/usr/bin/python3
import boto3
import os
import pandas as pd

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
REGION_NAME = os.getenv('AWS_DEFAULT_REGION')

# Create a DynamoDB client
dynamodb = boto3.client('dynamodb', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name=REGION_NAME)

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
print(day_ago)

scan_params_ts = {
    'TableName': table_name,
    'FilterExpression': '#ts > :ts_day_ago',
    'ExpressionAttributeNames': {'#ts': 'timestamp'},
    'ExpressionAttributeValues': {':ts_day_ago': {'S': day_ago}}
}


# Scan the table with the defined parameters
response = dynamodb.scan(**scan_params_ts)

# Print the items where the temperature is above 18
for item in response['Items']:
    print(item)
