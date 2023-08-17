---
title: Huyen - Designing ML Systems (Ch1)
created: Feb 2023
---

This is a really excellent book and I encourage you to go out and buy it!

#### Notes on Chapter 1 - Overview of Machine Learning Systems

- What is an ML system? It includes: 
    - business requirements
    - interfaces
    - data stack
    - model monitoring
    - infrastructure
- ML Ops is about bringing ML into production

**When to use ML?**

- ML is about learning complex patterns from existing data and then using these patterns to make predictions on unseen data
- Zero-shot learning is a problem set up where, at test time, the model has to make prediction about observations not from classes used in training
- For our team, where do we get the ground truth of particular tags?
- Unseen and training data should come from similar distributions 
- Enterprise applications might have higher accuracy but laxer latency requirements
- But customer-facing systems might have stricter latency requirements

**ML research vs production**

- production is more about stakeholder requirements, lower latency, and shifting datasets
    - Latency: the time between receiving a query and returning the result
- Production data is much messier and requires more preprocessing than standardised research datasets
- one way to deal with different objectives is to develop multiple models and combine them
- ensemble models a good example: used in research with high accuracy but end up being too complex to use in production
- research prioritises fast training but this might not be the same as fast inference

**ML in the real world**

- Fairness - rarely considered, no good metrics for fairness, and can perpetuate systemic biases
    - Members of minority groups might be particularly affected, but this would not show up on overall scores, as minority groups only make up a small part of the evaluation metrics
- Interpretability - mixed responses from people on whether they want more interpretable models, but users also might have a ‘right to explanation’
- “The vast majority of ML-related jobs will be, and already are, in productionizing ML”
- ML should learn more from SWE
    - SWE has separation of code and data but ML is more mixed together, and requires more vigilance about the data used in training and in deployment