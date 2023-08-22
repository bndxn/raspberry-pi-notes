---
title: Google - A friendly introduction to linear algebra for ML (ML Tech Talks)
created: Feb 2023
---

Linear algebra is often identified as one of the foundations of machine learning. 

I liked this quick overview from Google, available [here](https://www.youtube.com/watch?v=LlKAna21fLE). 


### Overview

The talks covers three areas in which linear algebra is important: 

1. Data representation
2. Vector embeddings
3. Dimensionality reduction


### 1. Data representation

* Representing information from the real world as vectors
* Totality of all of such vectors is the vector space
* A feature vector is simply one that represents the features of an object
* Images broken into pixels, grid is unzipped 
* Count of the appearance of particular words in different lists
* One-hot encoding for words or other categorical data, but for lots of categories this is sparse
* A sparse vector is one with lots of zeros 

**Dot products**

* Dot product helps understand similarity between vectors

```python
>>> import numpy as np
>>> a = [1, 0, 3]
>>> b = [7, 2, -1]
>>> np.dot(a,b)
4

>>> from numpy import linalg
>>> linalg.norm(a)
3.1622776601683795
>>> a_norm = a / linalg.norm(a)
>>> b_norm = b / linalg.norm(b)
>>> np.dot(a_norm, b_norm)
0.17213259316477408
```

* Dot products will be zero between similar one-hot encodings, which suggests they're not similar - one-hot doesn't capture similarity as spatial similarity

### 2. Vector embeddings

* An embedding is putting a vector in higher dimensions in lower dimensions
* How to find embeddings? One way is through matrix factorisations. A matrix represents a process of turning one vector into another one. 

**Matrix factorisation route**

* A matrix can be a transformation of an entire vector space
* Undoing matrix multiplication is matrix factorisation - are there smaller matrices than be multiplied together to get the answer?
* Every matrix can be factored - the factorisation is the singular value decomposition
* Every matrix can be written as the product of three smaller matrices
* SVD appears in lots of places
* For an original matrix, find smaller matrices U and V, so that taking their product gives the original matrix

**Neural network route**

* Put the original data into the neural network, and the outcome can be a vector embedding
* In either case you want to keep information

### 3. Dimensionality reduction

* Find the eigenvectors, aka principal components
* Eigenvectors for a matrix are those that do not have their direction changed when transformed by that matrix, but which might scale 
* The eigenvalue is the scaling factor
* Eigenvectors encode valuable information
* You might have n data points in m-dim space, which are clustered around a line or lower-dimensional subspace

**How to do PCA?**

* Organise points into an mxn matrix A, then compute the eigenvectors of the matrix multiplied by its transpose, $AA^{t}$. 
* Then the data points are centered by subtracting the mean of each row
* Which eigenvector has the largest scaling factor (eigenvalue)? This one points the principal components/direction of the data
* So the eigenvectors tell you about inherent features of your data


### Summary

* Often data only occupies a small portion of large-dimensional vector space
* Working in smaller spaces increases efficiency
* Linear algebra helps you reduce dimensions and reveal relevant structure in the data