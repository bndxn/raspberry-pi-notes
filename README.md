# Raspberry Pi weather station

An application using real data, building a model, and deploying it using AWS.

Components
* RasPi and TemperHUM collecting temp and humidity readings
* DynamoDB bucket storing readings
* Flask application generating Plotly graphs, running on EC2 using Elastic Beanstalk, available at `bendixon.net`.
* Analysis of data done in notebooks in this repo

To do:
* Deploy the model as tf-lite. Previously deploying the full size model caused memory errors which were only fixed by changing the Elastic Beanstalk instance to a larger and more expensive one.


# Engineering additions

* Use of CodeBuild on the flask-website, but not yet, before deploying
* Testing using Pytest
* Makefile used for automating tests, formatting, and resolving dependencies
* Githooks (https://pre-commit.com/) used to resolve small code issues
* TODO : Use poetry for environment management

# Ideas

* How to run this retraining? Could run it on the Pi, then generate the saved model. Maybe another time could learn how to do this with AWS.
* How to get the saved model to the new repo? One option could be to run a bash script to copy the model into the flask-website repo, then run an automated commit - which should trigger the codebuild process!
