## In gradient descent, we go in the direction of the negative gradient. But why is this the direction of steepest descent?

Thanks to Khan Academy's video on this topic here: https://www.youtube.com/watch?v=TEB2z7ZlRAw. 

https://www.youtube.com/watch?v=KDHuWxy53uM

* We need to know that it's convex - otherwise how do we know we'll get a global solution?
* It might not be unique


We imagine a function of x and y, giving some output z. 

z = f(x,y)

You might remember how to calculate the dot product, but let's get the definition and what it means. 

The dot product is the projection of one vector onto another. 

So going back to our previous case, to find the vector in the direction of steepest ascent, we want to evaluate the directional gradient, i.e. how much the gradient moves in a particular direction. 

What is the directional gradient? Well it's the gradient, but just in a particular direction. So we want to work out how much the gradient is moving, but then project that onto one particular dimensions and see how much it moves. Sound familiar? 

We can just use the dot product. We want to dot the direction some vector moves in, with the gradient vector. 

And what about steepest ascent? Well that'll be when it's maximised. And when is the dot product of two unit vectors maximised? When they're pointing in the same direction? 

But what if we want to find out the direction of steepest *descent*? Well that's when things are most negative. When are two vectors most dissimilar? So moving from the projection being -> 1, to -> -1? Not perpendicular, but when the vector's in the opposite direction!

Ok putting it all together: 
* We want to find the direction of steepest descent
* The gradient tells us how much the output variable changes
* We can understand how much any vector contributes to that, by projecting it using the dot product, onto the gradient vector
* When is this minimsed? When it's the opposite direction to the gradient

