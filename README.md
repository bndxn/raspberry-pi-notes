# Raspberry Pi weather station

This repo is part of a system which collects temperature data, trains a model, and displays the results on a Flask website.

The end-to-end process is as follows:
1. Temperature and humidity readings are recorded on a Raspberry Pi using a bash script run every 10 minutes from the Pi
2. Readings are stored to DynamoDB every 10 minutes
3. Historic readings are queried, and used to train an ML model (an LSTM) to predict the temperature using past readings.
4. A web front end shows recent readings and uses the trained ML model to predict future values, hosted on AWS Elastic Beanstalk.

This repo contains the code for parts 1,2,3. Part 4 is stored in a different repo to separate the front-end from the training process, and to allow the web application to run on a smaller instance that does not also need to perform model training.

# Engineering additions

* CodePipeline is used on the flask-website repo to automatically update the image based on Github commits.
* Testing is now done Pytest
* Makefile used for automating tests, formatting, and resolving dependencies
* Githooks (https://pre-commit.com/) used to resolve small code issues

# Ideas

* How to run this retraining? Could run it on the Pi, then generate the saved model. Maybe another time could learn how to do this with AWS.
* How to get the saved model to the new repo? One option could be to run a bash script to copy the model into the flask-website repo, then run an automated commit - which should trigger the codebuild process!

# Formatting

The Makefile checks that the format is valid.


# Testing


# Logging

To do