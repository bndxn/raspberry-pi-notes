# Raspberry Pi weather station

Components
* RasPi and TemperHUM collecting temp and humidity readings
* DynamoDB bucket storing readings
* Flask application generating Plotly graphs, running on EC2 using Elastic Beanstalk, available at `pi.bendixon.net`.
* Deployment uses EB CLI: actuivate virtual env with `source eb-env/bin/activate`, then can test with `docker run -8080:8080 -v ~/.aws/credentials:/root/.aws/credentials docker_eb_v1`. Then can deploy with `eb deploy` from inside the directory. 

To-dos:
- [x] Speed up deployment process using Docker image (currently horribly hacky, running 

```
zip output.zip -r . -x "eb-env/*" "venv/*" "analysis/*" "output.zip" ".git/*" 
```

then uploading this to ELB)
- [] Speed up deployment yet further, explore CodePipeline
- [x] Analyse trends in data, see analysis tab
- [x] Experiment with forecasting models and find one to beat baseline
- [x] Deploy the LSTM to make predictions
- [] Add a daily and weekly box and whisker plot to get longer-term trends

## Articles I want to write

- Why is the negative gradient used in gradient descent?
- What is the probabilistic approach? 
- What is a generative approach?
- Explain L1 and L2 regularisation
- What is the kernel trick?


## Gotchas

MathJax [docs](https://docs.mathjax.org/en/latest/basic/mathematics.html).

``` 
The default math delimiters are $$...$$ and \[...\] for displayed mathematics, and \(...\) for in-line mathematics. Note in particular that the $...$ in-line delimiters are not used by default. That is because dollar signs appear too often in non-mathematical settings, which could cause some text to be treated as mathematics unexpectedly.
```

Notes on flask and markdown here https://flask-blogging.readthedocs.io/en/latest/#quick-start-example. 

The problem with some parts of the latex not rendering were because of the use of '_' as a special character. Can I get around that? Might be worth a new site, since this is all seeming like a hassle. Seems like e.g. jekyll sites wouldn't be in Python, hard to have so many other things going on. So maybe flask stays for now. 

https://flask-blogging.readthedocs.io/en/latest/#quick-start-example

## Formatting

* Code formatting is done with **Black**, 

## Stuart ideas - 17 August 2023

* Use kadru maybe?
* what's the biggest pain?
* Learn about code pipeline, code build, and cloud formation
* Newer approach is more modular 
* https://aws.amazon.com/cdk/ 
* https://github.com/bbc/auto-topic-api/blob/main/api/auto_topic_api/auto_topic_api_stack.py 