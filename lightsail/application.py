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


@application.route('/temp_ddb')
def temp_ddb():

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

   print('Timestamp response: json_normalise')
   df = pd.json_normalize(response_ts['Items'])
   df.sort_values(by='timestamp.S',inplace=True)
   
   # Not sure why this makes these graphs match the notebook ones
   df.to_csv('test.csv')
   df2 = pd.read_csv('test.csv')


   df = df2.rename(columns={'timestamp.S':'time', 'temperature.S':'temp',
                       'humidity.S':'hum'})

   
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


if __name__ == "__main__":
   application.run(host='0.0.0.0', port=8080)

