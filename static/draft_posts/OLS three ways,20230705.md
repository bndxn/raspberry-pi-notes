---
title: OLS - three ways
created: 15 June 2023
---


### Introduction 

[With endless thanks to Gilbert Strang]

Consider a task where you have some input data $$X$$, and your task is to predict the output $$y$$. This idea of a linear relationship between variables is found in many fields. 

$$y = wx + b$$

A more general form of this is where you can take in multiple inputs, $$x_1, x_2, ...$$. We can use the same approach to find the relationship between multiple input variables and an output variable. 

In linear regression, we work out the weights $$w_1, w_2, ...$$ in the equation $$y = x_1w_1 + x_2w_2 + ... + b$$

You may remember from school doing something like: 

$$S_{xy} = \sum{xy} - \frac{\sum{x}\sum{y}}{n}$$

$$S_{xx} = \sum{x^2} - \frac{(\sum{x})^2}{n}$$

Then to find the coefficients in our $$y = wx + b$$, we get out our calculators and do something like this:
$$w=S_{xx}/S_{xy}$$
$$b=\bar{y} - w\bar{x}$$

### Part 1: The geometric interpretation - projections

Consider projecting a point $$\mathbf{b}$$ onto the line given by the vector $$\mathbf{a}$$. 

- If we do this, there’ll be an error,  $$\mathbf{e}=\mathbf{b}-\mathbf{p}$$, shown by the dashed line, of the difference between the projected point and the original point 
- And the projected point $$\mathbf{p}$$ will be somewhere along $$\mathbf{a}$$, so it’ll be $$\mathbf{p}=\mathbf{\hat{x}}\mathbf{a}$$
- The closest point on the line $$\mathbf{a}$$ to the original $$\mathbf{b}$$ will be when there’s a 90 degree angle between $$\mathbf{p}$$ and $$\mathbf{a}$$. This is where the minimisation happens.


Writing this idea down:

$$\mathbf{a}\perp(\mathbf{e})$$
$$\mathbf{a}\perp(\mathbf{b}-\mathbf{p})$$
$$\mathbf{a}\cdot(\mathbf{b}-\mathbf{p})=0$$

We defined $$\mathbf{p}=\mathbf{\hat{x}}\mathbf{a}$$, so 

$$\mathbf{a}\cdot(\mathbf{b}-\mathbf{\hat{x}}\mathbf{a})=0$$
$$\mathbf{a}^T\mathbf{b}-\mathbf{a}^T\mathbf{a}\mathbf{\hat{x}}=0$$

$$\mathbf{\hat{x}} = \frac{\mathbf{a}^T\mathbf{b}}{\mathbf{a}^T\mathbf{a}}$$

This would give us the factor $$\mathbf{\hat{x}}$$ in $$\mathbf{p}=\mathbf{\hat{x}}\mathbf{a}$$.