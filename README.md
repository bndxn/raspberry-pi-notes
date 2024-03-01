# Raspberry Pi weather station

This repo is part of a system which collects temperature data, trains a model, and displays the results on a Flask website.

The end-to-end process is as follows:
1. Temperature and humidity readings are recorded from Raspberry Pi, and uploaded to DynamoDB using a bash script run every 10 minutes from the Pi
2. An LSTM model is trained (previously with notebooks, in the future with an automated pipeline) using historic readings, and the model is converted to tensorflow-lite format
3. The model is deployed on the [flask website](https://github.com/bndxn/flask-website). 
4. A web front end shows recent readings and uses the trained ML model to predict future values, hosted on AWS Elastic Beanstalk.

This repo contains the code for parts 1 and 2. Parts 3 and 4 is stored in a different repo to separate the front-end from the training process, and to allow the web application to run on a smaller instance that does not also need to perform model training.

## Engineering additions
A few things I've added:
* CodePipeline is used on the flask-website repo to automatically update the image based on Github commits.
* Testing is now done using pytest
* Makefile used for automating tests, formatting, and resolving dependencies
* [Githooks](https://pre-commit.com/) used to resolve small code issues

## To do
* Automate model retraining, maybe using Sagemaker, or possibly just set up a bash script to retrain/move/commit the other model, or find some better way of doing this 
