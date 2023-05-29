## Google - A friendly introduction to linear algebra for ML (ML Tech Talks)

https://www.youtube.com/watch?v=LlKAna21fLE

### Overview
Three topics covered: 
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
* A matrix can be a transformation of an entire vector space
* Undoing matrix multiplication is matrix factorisation - are there smaller matrices than be multiplied together to get the answer?
* Every matrix can be factored - the factorisation is the singular value decomposition
* Every matrix can be written as the product of three smaller matrices
* SVD appears in lots of places
* The rows and columns for the components of the SVD should be similar 