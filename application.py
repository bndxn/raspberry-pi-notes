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

application = Flask(__name__)

@application.route('/')
def index():
   return render_template('index.html')

@application.route('/latex')
def latex():
   latex_snippet = r'The normal distribution: \(\ (x) = \frac{1}{\sigma \sqrt{2\pi}} e^{-\frac{(x - \mu)^2}{2\sigma^2}}\) !!!'
   return render_template('latex_index.html', latex_snippet=latex_snippet)


@application.route('/temp_local')
def temp_local():
   
   # For now, trying out local version
   df = pd.read_csv('local_copy_test2.csv', skiprows=0, index_col=0)
   df.rename(columns={'0':'temp', '1':'hum', '2': 'time'},inplace=True)

   fig = make_subplots(specs=[[{"secondary_y": True}]])

   fig.add_trace(
    go.Scatter(x=df['time'],y=df['temp'], name="Temperature", mode='markers'),
    secondary_y=False,
   )

   fig.add_trace(
    go.Scatter(x=df['time'],y=df['hum'], name="Humidity", mode='markers'),
    secondary_y=True,
   )

   fig.update_layout(
    title_text="Temperature and humidity over time"
   )

   fig.update_layout(
    autosize=False,
     yaxis = dict(
         tickmode = 'array',
         tickvals = np.arange(0,50,0.5)),
     yaxis_tickformat=' ',
    )

   # Set x-axis title
   fig.update_xaxes(title_text="Time")

   # Set y-axes titles
   fig.update_yaxes(title_text="<b>Temperature</b>", title_font_color='blue', secondary_y=False)
   fig.update_yaxes(title_text="<b>Humidity</b>", title_font_color='red', secondary_y=True)

   graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
   return render_template('notdash.html', graphJSON=graphJSON)


@application.route('/last_day')
def last_day():

   client = boto3.client('dynamodb', region_name='us-east-1')
   
   table_name = 'pi-temperature-readings'

   day_ago = str(pd.Timestamp.now() - pd.Timedelta(days=1))

   scan_params = {
         'TableName': table_name,
         'FilterExpression': '#ts > :day_ago',
         'ExpressionAttributeNames': {'#ts': 'timestamp'},
         'ExpressionAttributeValues': {':day_ago': {'S': day_ago}}
   }

   response_ts = client.scan(**scan_params)

   df = pd.json_normalize(response_ts['Items'])
   df.sort_values(by='timestamp.S',inplace=True)
   
   # Not sure why this makes these graphs match the notebook ones
   df.to_csv('last_day.csv')
   del df
   df = pd.read_csv('last_day.csv')


   df.rename(columns={'timestamp.S':'time', 'temperature.S':'temp',
                       'humidity.S':'hum'},inplace=True)

   
   fig = make_subplots(specs=[[{"secondary_y": True}]])

   fig.add_trace(
    go.Scatter(x=df['time'],y=df['temp'], name="Temperature", mode='markers'),
    secondary_y=False,
   )

   fig.add_trace(
    go.Scatter(x=df['time'],y=df['hum'], name="Humidity", mode='markers'),
    secondary_y=True,
   )

   fig.update_layout(
    title_text="Temperature and humidity over time"
   )

   fig.update_layout(
    autosize=False
    )

   # Set x-axis title
   fig.update_xaxes(title_text="Time")

   # Set y-axes titles
   fig.update_yaxes(title_text="<b>Temperature</b>", title_font_color='blue', secondary_y=False)
   fig.update_yaxes(title_text="<b>Humidity</b>", title_font_color='red', secondary_y=True)

   graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
   return render_template('notdash.html', graphJSON=graphJSON)


@application.route('/last_week')
def last_week():
   return render_template('index.html')



@application.route('/all_time')
def all_time():

   client = boto3.client('dynamodb', region_name='us-east-1')
   
   table_name = 'pi-temperature-readings'

   # First recordings on the pi were from 2023-04-21
   start_date = str(pd.Timestamp('2023-04-21'))

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
   fig.show()

   graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
   return render_template('notdash.html', graphJSON=graphJSON)


if __name__ == "__main__":
   application.run(host='0.0.0.0', port=8080)

