from flask import Flask, render_template
import pandas as pd
import json
import plotly
import plotly.express as px
import boto3

application = Flask(__name__)

@application.route('/')
def notdash():
   df = pd.DataFrame({
      'Fruit': ['Apples', 'Oranges', 'Bananas', 'Apples', 'Oranges', 'Bananas'],
      'Amount': [4, 1, 2, 2, 4, 5],
      'City': ['SF', 'SF', 'SF', 'Montreal', 'Montreal', 'Montreal']
   })
   fig = px.bar(df, x='Fruit', y='Amount', color='City',    barmode='group')
   graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
   return render_template('notdash.html', graphJSON=graphJSON)

@application.route('/line')
def notdash_line():
   df = pd.DataFrame({
      'x': [1, 2, 3, 4, 5, 6],
      'y': [1, 4, 9, 16, 25, 36]
   })
   fig = px.line(df, x='x', y='y')
   graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
   return render_template('notdash.html', graphJSON=graphJSON)

@application.route('/temp_local')
def notdash_temp_local():
   
   # For now, trying out local version
   df = pd.read_csv('local_copy_test2.csv', skiprows=0, index_col=0)
   df.rename(columns={'0':'temp', '1':'hum', '2': 'time'},inplace=True)

   fig = px.line(df, x='temp', y='time')
   graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
   return render_template('notdash.html', graphJSON=graphJSON)


@application.route('/temp_aws')
def notdash_temp_aws():


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

