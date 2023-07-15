from flask import Flask, render_template, jsonify
import pandas as pd
import plotly.graph_objs as go
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import plotly
import plotly.express as px
import boto3
import numpy as np
from helpers import ddb_connection, graphers
import joblib
from tensorflow import keras


application = Flask(__name__)

@application.route('/')
def index():
   return render_template('index.html')

@application.route('/latex')
def latex():
   article = {
      'article': 'Testing multiline',
      'text': """Let \(\mathbf{a}\) and \(\mathbf{b}\) be vectors in an inner product space. We want to show that \(|\langle \mathbf{a}, \mathbf{b} \rangle| \leq \|\mathbf{a}\| \cdot \|\mathbf{b}\|\). 
                  Consider the real function \(f(t) = \|\mathbf{a} - t\mathbf{b}\|^2\), where \(t\) is a real scalar.

                  Expanding the norm expression, we have:

                  \[
                  f(t) = \|\mathbf{a} - t\mathbf{b}\|^2 = \langle \mathbf{a} - t\mathbf{b}, \mathbf{a} - t\mathbf{b} \rangle
                  \]

                  Using the linearity and conjugate symmetry properties of inner products, we can expand the above expression as:

                  \[
                  f(t) = \langle \mathbf{a}, \mathbf{a} \rangle - t \langle \mathbf{a}, \mathbf{b} \rangle - \overline{t} \langle \mathbf{b}, \mathbf{a} \rangle + t\overline{t} \langle \mathbf{b}, \mathbf{b} \rangle
                  \]

                  Simplifying further, we obtain:"""}



   return render_template('latex.html', latex_snippet=article)


@application.route('/about')
def about():
   return render_template('about.html')

@application.route('/blog')
def blog():
   return render_template('blog.html')

@application.route('/live_data')
def live_data():

   day_ago = str(pd.Timestamp.now() - pd.Timedelta(days=1))

   connection = ddb_connection.DynamoResource()

   df = ddb_connection.DynamoResource.query(connection, day_ago)

   fig = graphers.overlapping_temperature_and_humidity(df)

   baseline_forecast = df['temperature'].iloc[-1]

   import os
   print(os.getcwd())
   model = keras.models.load_model('static/basic_model.keras')
   input_to_model = np.array(df['temperature'].iloc[-12:]).reshape((1, 12, 1))
   predictions = model.predict(input_to_model)
   print(len(predictions))


   graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
   return render_template('notdash.html', 
            graphJSON=graphJSON, 
            header='Last day', 
            description='Temperature and humidity over the last day',
            baseline_forecast=baseline_forecast,
            model_forecast=predictions)



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

