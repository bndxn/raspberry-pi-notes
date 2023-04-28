from flask import Flask, render_template
import pandas as pd
import json
import plotly
import plotly.express as px
import boto3

application = Flask(__name__)

@application.route('/')
def index():
   return render_template('index.html')


@application.route('/temp_local')
def temp_local():
   
   # For now, trying out local version
   df = pd.read_csv('local_copy_test2.csv', skiprows=0, index_col=0)
   df.rename(columns={'0':'temp', '1':'hum', '2': 'time'},inplace=True)

   fig = px.line(df, x='time', y='temp')
   graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
   return render_template('notdash.html', graphJSON=graphJSON)


@application.route('/temp_s3')
def temp_s3():

   s3 = boto3.resource('s3')
   
   s3.Bucket('pi-temperature-readings').download_file('test2.csv','local_copy_test3.csv')
   
   # Downloading it as no. 3 to the local directory, let's see what happens
   df = pd.read_csv('local_copy_test3.csv', skiprows=0, index_col=0)
   df.rename(columns={'0':'temp', '1':'hum', '2': 'time'},inplace=True)

   fig = px.line(df, x='time', y='temp')
   graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
   return render_template('notdash.html', graphJSON=graphJSON)


@application.route('/temp_ddb')
def temp_ddb():

   client = boto3.client('dynamodb')
   
   table_name = 'pi-temperature-readings'

   day_ago = str(pd.Timestamp.now() - pd.Timedelta(days=1))

   scan_params = {
         'TableName': table_name,
         'FilterExpression': '#ts > :day_ago',
         'ExpressionAttributeNames': {'#ts': 'timestamp'},
         'ExpressionAttributeValues': {':day_ago': {'S': day_ago}}
   }

   response_ts = client.scan(**scan_params)

   print('Timestamp response: json_normalise')
   df = pd.json_normalize(response_ts['Items'])
   df.sort_values(by='timestamp.S',inplace=True)
   
   # Not sure why this makes these graphs match the notebook ones
   df.to_csv('test.csv')
   df2 = pd.read_csv('test.csv')
   fig = px.scatter(df2, x='timestamp.S', y='temperature.S')
   graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
   return render_template('notdash.html', graphJSON=graphJSON)

if __name__ == "__main__":
   application.run(host='0.0.0.0', port=8080)

