# Notes on a weather station idea

Three general areas of this repo: 

1. Collecting data (takes USB readings, plus uploads them to S3) - currently a Python file, should in future be a cronjob `collect_temp_data.py` and `temper.py`
2. Generating docker container for website using Flask and Plotly, hosted on AWS Lightsail, started in `download_temp_data.py`
3. Misc potentially useful code from various places

Next steps:
* Install docker on the pi, and also awscli and the lightsail plugin
* Test accessing the S3 bucket from within a docker container, and generating a plotly graph
* Push the docker container-image to lightsail and see if it can access S3
