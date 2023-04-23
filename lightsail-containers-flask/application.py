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


@application.route('/temp_aws')
def temp_aws():

   s3 = boto3.resource('s3')
   
   s3.Bucket('pi-temperature-readings').download_file('test2.csv','local_copy_test3.csv')
   
   # Downloading it as no. 3 to the local directory, let's see what happens
   df = pd.read_csv('local_copy_test3.csv', skiprows=0, index_col=0)
   df.rename(columns={'0':'temp', '1':'hum', '2': 'time'},inplace=True)

   fig = px.line(df, x='time', y='temp')
   graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
   return render_template('notdash.html', graphJSON=graphJSON)




if __name__ == "__main__":
   application.run(host='0.0.0.0', port=8080)

