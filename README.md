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

## Notes on the blog 

- Looking for a way to store articles on the web so that I can embed HTML and LaTeX, and also hopefully fairly easy to use
- Settling on YAML and markdown, e.g. 

```
---
title: Huyen - Designing ML Systems (Ch1&2)
created: Feb 2023
---

## Overview of ML systems

$$y = wx + b$$

```

- How to store these online? Want to be able to query data source without loading everything, and also in the future want to be able to search by tag. One option is storing metadata in the file names.
- GPT4 suggests articles stored in S3, and metadata stored in DDB. A bit more convoluted but think I will do as I want to be able to search by tags and rearrange articles in future. 

