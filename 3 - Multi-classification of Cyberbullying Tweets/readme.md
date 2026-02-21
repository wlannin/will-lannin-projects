# 3 - Multi-classification of Cyberbullying Tweets
TRIGGER WARNING this dataset contains several uncensored slurs and all-round BAD words so read at your own danger. This exercise was purely academic for me and I found the dataset here: https://www.kaggle.com/datasets/pradeepjswl/cyberbullying-tweets

## Summary of my work on this project (if you don't have time to read the notebook!)
We have managed to very quickly arrive at a 6-class classifier that can take unseen tweets and provide a reliable prediction of how likely the tweet is to contain bullying of 4 specific types (religion, gender, age, ethnicity), or some 'other' type of bullying not specified, or no bullying at all.

We did this by fitting 5 separate binary models (logistic regresions, using tf-idf to engineer features from the tweets). The 5 models were trained on the entire train dataset, and the binary target for these 5 models were as follows:
1. indicator of whether tweet contains cyberbullying_type='religion'
2. indicator of whether tweet contains cyberbullying_type='gender'
3. indicator of whether tweet contains cyberbullying_type='age'
4. indicator of whether tweet contains cyberbullying_type='ethnicity'
5. indicator of whether tweet contains cyberbullying_type='other_cyberbullying'

The binary models predicting specific bullying types (religion, gender, age, ethnicity) performed extremely well and only required 7-40 features (thanks to L1 regularisation on the logistic regressions). 

The binary model for 'other_cyberbullying' was less predictive, and required inclusion of 179 features to get satisfactory enough performance. The impact of this can be seen in the confusion matrices in section 3.3; several cases that my model predicted to be 'other_cyberbullying' were actually 'not_cyberbullying', and vice versa!

The technique to combine our 5 binary models into a final prediction is based on the predicted probabilities calculated like so:

$$P(Y = k \mid \mathbf{x}) = \frac{e^{\mathbf{x}^\top \boldsymbol{\beta}_k}}{1 + \sum_{j=1}^{K-1} e^{\mathbf{x}^\top \boldsymbol{\beta}_j}}$$

$$P(Y = K \mid \mathbf{x}) = \frac{1}{1 + \sum_{j=1}^{K-1} e^{\mathbf{x}^\top \boldsymbol{\beta}_j}}$$

For our example, K=6 and the class K shown at the bottom is 'not_cyberbullying'.
