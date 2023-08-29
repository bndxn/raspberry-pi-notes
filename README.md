# Raspberry Pi weather station

Components
* RasPi and TemperHUM collecting temp and humidity readings
* DynamoDB bucket storing readings
* Flask application generating Plotly graphs, running on EC2 using Elastic Beanstalk, available at `pi.bendixon.net`.
* Deployment uses EB CLI: actuivate virtual env with `source eb-env/bin/activate`, then can test with `docker run -8080:8080 -v ~/.aws/credentials:/root/.aws/credentials docker_eb_v1`. Then can deploy with `eb deploy` from inside the directory. 

To-dos:
- [x] Speed up deployment process using Docker image (currently horribly hacky, running 

```
zip output.zip -r . -x "eb-env/*" "app_env/*" "analysis/*" "output.zip" ".git/*" 
```

then uploading this to ELB)
- [] Speed up deployment yet further, explore CodePipeline
- [x] Analyse trends in data, see analysis tab
- [x] Experiment with forecasting models and find one to beat baseline
- [x] Deploy the LSTM to make predictions
- [] Add a daily and weekly box and whisker plot to get longer-term trends



## Stuart ideas - 17 August 2023

* Use kadru maybe?
* what's the biggest pain?
* Learn about code pipeline, code build, and cloud formation
* Newer approach is more modular 
* https://aws.amazon.com/cdk/ 
* https://github.com/bbc/auto-topic-api/blob/main/api/auto_topic_api/auto_topic_api_stack.py 

