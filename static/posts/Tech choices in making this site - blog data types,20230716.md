---
title: Tech choices - blog data types
created: 18 August 2023
---

I'm looking for a way to store articles so that I can embed HTML tags and LaTeX when they're rendered. To get me to actually post, I should make this as easy to use as possible. 

#### Some ideas
* JSON - my first try, got a load of errors about escape characters from LaTeX. 
* CSV - not good for multiline, harder to read, plus I'd want to have escape characters that might overlap 
* Plaintext - could have multilines, but lack of structure means I'd need to do a load of splitting on defined characters
* Markdown and YAML - seems like the solution! Can split the item, and markdown is an easy format to write in

### Example snippet

It's like this, but the dashes are together, not spaced out. I've separated them as this is the section separator I'm using. 

```
- - - 
title: Huyen - Designing ML Systems (Ch1&2)
created: Feb 2023
- - - 

## Overview of ML systems

$$y = wx + b$$

```

### Storing online
- How to store these online? Want to be able to query data source without loading everything, and also in the future want to be able to search by tag. One option is storing metadata in the file names.
- GPT4 suggests articles stored in S3, and metadata stored in DDB. A bit more convoluted but think I will do as I want to be able to search by tags and rearrange articles in future.