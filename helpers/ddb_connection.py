# This file should provide the DDB querying tools for application.py, but should also work as a standalone

#!/usr/bin/python3
import os
import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
import pandas as pd


class DynamoResource:
    def __init__(self):
        self.dynamodb = boto3.client(
            "dynamodb",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name="us-east-1",
        )

    def query(self, since_timestamp=None):
        table_name = "pi-temperature-readings"

        if since_timestamp == None:
            start_date = str(pd.Timestamp("2023-04-28"))
        else:
            start_date = since_timestamp

        scan_params = {
            "TableName": table_name,
            "FilterExpression": "#ts > :start_date",
            "ExpressionAttributeNames": {"#ts": "timestamp"},
            "ExpressionAttributeValues": {":start_date": {"S": start_date}},
        }

        response_ts = self.dynamodb.scan(**scan_params)

        df = pd.json_normalize(response_ts["Items"])
        df.sort_values(by="timestamp.S", inplace=True)

        df.rename(
            columns={
                "humidity.S": "humidity",
                "temperature.S": "temperature",
                "timestamp.S": "timestamp",
            },
            inplace=True,
        )

        df[["humidity", "temperature"]] = df[["humidity", "temperature"]].apply(
            pd.to_numeric
        )

        return df


def df_stored_locally():
    data = [
        [56.15, 20.46, "2023-05-13 03:30:04.185467"],
        [56.02, 20.46, "2023-05-13 03:40:04.646393"],
        [55.97, 20.48, "2023-05-13 03:50:04.093586"],
        [56.07, 20.40, "2023-05-13 04:00:04.536077"],
    ]

    df = pd.DataFrame(data)

    df.rename(columns={0: "temperature", 1: "humidity", 2: "timestamp"}, inplace=True)
    df[["humidity", "temperature"]] = df[["humidity", "temperature"]].apply(
        pd.to_numeric
    )
    df["timestamp"] = df["timestamp"].apply(pd.Timestamp)

    return df


if __name__ == "__main__":
    dynamoresource = DynamoResource()
    dynamoresource.query()
    print("Done")
