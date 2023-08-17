from flask import Flask, render_template, abort, jsonify
from werkzeug.exceptions import abort
import pandas as pd
#import plotly.graph_objs as go
#import plotly.graph_objects as go
#from plotly.subplots import make_subplots
import json
import plotly
import plotly.express as px
#import boto3
import numpy as np
from helpers import ddb_connection, graphers
#from tensorflow import keras
import os
from datetime import datetime
import yaml
import markdown2


application = Flask(__name__)

@application.route('/')
def index():
   return render_template('index.html')


def get_post(post_id):
   for num, post_name in enumerate(os.listdir('static/posts/')):
      if num == post_id:
         with open(f'static/posts/{post_name}', 'r') as f:
            content = f.read()
            
            # Split YAML front matter from markdown content
            front_matter, markdown_content = content.split('---')[1:3]
            
            # Parse YAML and Markdown
            post_metadata = yaml.safe_load(front_matter.strip())
            post_html_content = markdown2.markdown(markdown_content.strip(),
                                                   extras=["fenced-code-blocks"])
            
            post_data = {
                'title': post_metadata['title'],
                'created': post_metadata['created'],
                'content': post_html_content
            }
            
            return post_data
   abort(404)

@application.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)


@application.route('/about')
def about():
   return render_template('about.html')

@application.route('/blog')
def blog():
   
   posts = []

   for post in os.listdir('static/posts/'):
      title, _ = post.split(",")
      date = _.split(".")[0]

      formatted_date = datetime.strptime(date, "%Y%m%d").strftime("%B %d, %Y")

      posts.append({'title': title, 'created': formatted_date})      

   return render_template('blog.html', posts=posts, enumerate=enumerate)

@application.route('/live_data')
def live_data():

   day_ago = str(pd.Timestamp.now() - pd.Timedelta(days=1))

   connection = ddb_connection.DynamoResource()

   df = ddb_connection.DynamoResource.query(connection, day_ago)

   fig = graphers.overlapping_temperature_and_humidity(df)

   baseline_forecast = df['temperature'].iloc[-1]

   print(os.getcwd())
   model = keras.models.load_model('static/basic_model.keras')
   input_to_model = np.array(df['temperature'].iloc[-12:]).reshape((1, 12, 1))
   predictions = model.predict(input_to_model)[0][0]

   temp_mean =  21.735619
   temp_std = 1.946606

   predictions = (predictions * temp_std ) + temp_mean

   graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
   return render_template('notdash.html', 
            graphJSON=graphJSON, 
            header='Last day', 
            description='Temperature and humidity over the last day',
            baseline_forecast=baseline_forecast,
            model_forecast=np.round(predictions,2))


@application.route('/all_time')
def all_time():

   connection = ddb_connection.DynamoResource()

   df = ddb_connection.DynamoResource.query(connection)

   fig = px.scatter(df, x='timestamp', y='temperature')
   
   fig.update_yaxes(title_text='Temperature')
   fig.update_xaxes(title_text='Time')


   graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
   return render_template('notdash.html', graphJSON=graphJSON,
            header='Temperature only', description='Temperature only, since start of measurements.')


if __name__ == "__main__":
   application.run(host='0.0.0.0', port=8080)

