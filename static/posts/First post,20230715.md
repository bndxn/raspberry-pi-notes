Consider a task where you have some input data \(X\), and your task is to predict the output \(y\). This idea of a linear relationship between variables is found in many fields. 

\[y = wx + b\]

A more general form of this is where you can take in multiple inputs, \(x_1, x_2, ...\). We can use the same approach to find the relationship between multiple input variables and an output variable. 

In linear regression, we work out the weights \(w_1, w_2, ...\), in the equation \(y = x_1w_1 + x_2w_2 + ... + b\).

You may remember from school doing something like: 

\[S_{xy} = \sum{xy} - \frac{\sum{x}\sum{y}}{n}\]

\[S_{xx} = \sum{x^2} - \frac{(\sum{x})^2}{n}\]

Then to find the coefficients in our \(y = wx + b\), we get out our calculators and do something like this:
\(w = \frac{S_{xx}}{S_{xy}}\)
\(b = \bar{y} - w\bar{x}\)


