# Raspberry Pi weather station

Components
* RasPi and TemperHUM collecting temp and humidity readings
* DynamoDB bucket storing readings
* Flask application generating Plotly graphs, running on EC2 using Elastic Beanstalk, available at `pi.bendixon.net`.


To-dos:
* Speed up deployment process using CodePipeline and Docker image (currently running `zip output.zip -r .` then uploading this to ELB)
* Analyse trends in data, see analysis tab
* Experiment with forecasting models

## Gotchas

MathJax [docs](https://docs.mathjax.org/en/latest/basic/mathematics.html).

``` 
The default math delimiters are $$...$$ and \[...\] for displayed mathematics, and \(...\) for in-line mathematics. Note in particular that the $...$ in-line delimiters are not used by default. That is because dollar signs appear too often in non-mathematical settings, which could cause some text to be treated as mathematics unexpectedly.
```