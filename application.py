from flask import Flask, render_template
import pandas as pd
import plotly.graph_objs as go
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import plotly
import plotly.express as px
import boto3
import numpy as np
from helpers import graphers, s3_connection

application = Flask(__name__)

@application.route('/')
def index():
   return render_template('index.html')


@application.route('/temp_local')
def temp_local():
   
   # For now, trying out local version
   df = pd.read_csv('local_copy_test2.csv', skiprows=0, index_col=0)
   df.rename(columns={'0':'temp', '1':'hum', '2': 'time'},inplace=True)

   fig = graphers.generate_time_and_humidity_figure(df)

   graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
   return render_template('notdash.html', graphJSON=graphJSON)


@application.route('/last_day')
def last_day():

   day_ago = str(pd.Timestamp.now() - pd.Timedelta(days=1))


   scan_params = {
         'TableName': table_name,
         'FilterExpression': '#ts > :day_ago',
         'ExpressionAttributeNames': {'#ts': 'timestamp'},
         'ExpressionAttributeValues': {':day_ago': {'S': day_ago}}
   }

   response_ts = client.scan(**scan_params)

   df = pd.json_normalize(response_ts['Items']
                        ).rename(
                        columns={'timestamp.S':'timestamp', 
                                 'temperature.S':'temperature',
                                 'humidity.S':'humidity'}
                        ).sort_values(by='time')

   # Using separate file for this
   fig = px.scatter(df, x="timestamp", y=["humidity","temperature"], 
                    title='Past day\'s humidity and temperature!')


   graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
   return render_template('notdash.html', graphJSON=graphJSON)


@application.route('/last_week')
def last_week():
   return render_template('index.html')


@application.route('/all_time')
def all_time():

   client = boto3.client('dynamodb', region_name='us-east-1')
   
   table_name = 'pi-temperature-readings'

   # First recordings on the pi were from 2023-04-21, but complete from 28th
   start_date = str(pd.Timestamp('2023-04-28'))

   scan_params = {
         'TableName': table_name,
         'FilterExpression': '#ts > :start_date',
         'ExpressionAttributeNames': {'#ts': 'timestamp'},
         'ExpressionAttributeValues': {':start_date': {'S': start_date}}
   }

   response_ts = client.scan(**scan_params)

   df = pd.json_normalize(response_ts['Items'])
   df.sort_values(by='timestamp.S',inplace=True)

   df.to_csv('all_time.csv')
   del df
   df = pd.read_csv('all_time.csv')

   df.rename(columns={'humidity.S': 'humidity',
                   'temperature.S':'temp',
                   'timestamp.S':'timestamp'},inplace=True)

   fig = px.scatter(df, x="timestamp", y=["humidity","temp"], 
                    title='All-time humidity and temperature in the grove!')

   graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
   return render_template('notdash.html', graphJSON=graphJSON)


if __name__ == "__main__":
   application.run(host='0.0.0.0', port=8080)

