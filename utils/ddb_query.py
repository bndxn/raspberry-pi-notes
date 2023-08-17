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
            region_name=os.getenv("AWS_DEFAULT_REGION"),
        )

    def query_all_time(self):
        table_name = "pi-temperature-readings"

        start_date = str(pd.Timestamp("2023-04-28"))

        scan_params = {
            "TableName": table_name,
            "FilterExpression": "#ts > :start_date",
            "ExpressionAttributeNames": {"#ts": "timestamp"},
            "ExpressionAttributeValues": {":start_date": {"S": start_date}},
        }

        response_ts = self.dynamodb.scan(**scan_params)

        print("Timestamp response: json_normalise")
        df = pd.json_normalize(response_ts["Items"])
        df.sort_values(by="timestamp.S", inplace=True)
        # df.to_csv('../analysis/ddb_output.csv')
        print(df)


if __name__ == "__main__":
    dynamoresource = DynamoResource()
    dynamoresource.query_all_time()
    print("Done")
