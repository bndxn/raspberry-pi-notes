
# Source article: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/example_dynamodb_PutItem_section.html

# Source code: https://github.com/awsdocs/aws-doc-sdk-examples/blob/main/python/example_code/dynamodb/GettingStarted/scenario_getting_started_movies.py#L151

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
from question import Question

class Readings():
  
    def __init__(self, dyn_resource):
      """
      :param dyn_resource: A Boto3 DynamoDB resource.
      """
      self.dyn_resource = dyn_resource
      self.table = None
      
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
        logger.error(
          "Couldn't add reading at % to table. Here's why: %s: %s",
          err.response['Error']['Code'], err.response['Error']['Message'])
     
    # Scanning for readings: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/example_dynamodb_Scan_section.html
 
    def get_readings(self, time_range):
    """
    Scans for movies that were released in a range of years.
    Uses a projection expression to return data for each movie.
    :param year_range: The range of years to retrieve.
    :return: The list of movies released in the specified years.
    """
    readings = []
    scan_kwargs = {
        'FilterExpression': Key('year').between(year_range['first'], year_range['second']),
        # doesn't dynanoDB convert all timestamps to strings?
        'ProjectionExpression': "#yr, title, info.rating",
        'ExpressionAttributeNames': {"#yr": "year"}}
    try:
        done = False
        start_key = None
        while not done:
            if start_key:
                scan_kwargs['ExclusiveStartKey'] = start_key
            response = self.table.scan(**scan_kwargs) # self.table.scan(**scan_kwargs) uses a dictionary as an argument?
            readings.extend(response.get('Items', [])) # extend takes another list as an argument, firstlist.extend([additions])
            start_key = response.get('LastEvaluatedKey', None)
            done = start_key is None
    except ClientError as err:
        logger.error(
            "Couldn't scan for readings. Here's why: %s: %s",
            err.response['Error']['Code'], err.response['Error']['Message'])
        raise

    return readings
      


      

