# Use this to control collecting temperatures and saving them to a DB
#!/usr/bin/python3

import os
import boto3
from botocore.exceptions import ClientError
from temper import Temper
import pandas as pd


class DDBReadings:
    def __init__(self):
        """
        :param dyn_resource: A Boto3 DynamoDB resource.
        """
        AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
        AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
        REGION_NAME = os.getenv("AWS_DEFAULT_REGION")

        dyn_resource = boto3.resource(
            "dynamodb",
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name="us-east-1",
        )
        self.table = dyn_resource.Table("pi-temperature-readings")

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
                    "timestamp": datetime,
                    "temperature": temperature,
                    "humidity": humidity,
                }
            )
        except ClientError as err:
            print(err)


readings = list[Temper]()


def upload_data_DDB(reading):
    print("Uploading to DDB")
    upload = DDBReadings()
    datetime = str(pd.Timestamp.now().round("1min"))
    temperature = reading[0]
    humidity = reading[1]
    print(f"DDB upload: Datetime: {datetime}, temp: {temperature}, hum: {humidity}")
    upload.add_reading(datetime, temperature, humidity)


def temper_ddb():
    # Create an instance of the class
    temper = Temper()
    # Call the instance objects
    reading = temper.main()
    # Do the upload
    upload_data_DDB(reading)


if __name__ == "__main__":
    temper_ddb()
