# Raspberry Pi weather station

Components
* RasPi and TemperHUM collecting temp and humidity readings
* DynamoDB bucket storing readings
* Flask application generating Plotly graphs, running on EC2 using Elastic Beanstalk, available at `pi.bendixon.net`.


To-dos:
* Speed up deployment process using CodePipeline and Docker image (currently running `zip output.zip -r .` then uploading this to ELB)
* Analyse trends in data, see analysis tab
* Experiment with forecasting models