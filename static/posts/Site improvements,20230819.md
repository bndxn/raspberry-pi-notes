---
title: Site improvements
created: 19 August 2023
---

There's a lot of ways I want to improve this site, if I had the time. Some are here:

* Sort out the deployment process, to use something like CodeBuild or CodePipeline. If I could commit to a branch and get instant deployment, that would be great
* Move the article storage from local to DDB and S3, with DDB for the metadata and S3 for the content
* Store images in an S3 bucket and reference them in the articles
* Use a smaller model for the pi weather forecasting stuff, maybe use tensorflow-lite instead of (previously) loading the full shazam of tf and then needing a bigger and more expensive instance
* Set up SSL
* Restructure the site to use a bunch of lambdas, following the serverless architecture hype, possibly reducing cost
* Allow for comments on blog posts