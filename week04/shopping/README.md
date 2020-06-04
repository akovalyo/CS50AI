# Project 4a: Shopping

Write an AI to predict whether online shopping customers will complete a purchase.

The goal of the project is to build a nearest-neighbor classifier using information about a user — how many pages they’ve visited, whether they’re shopping on a weekend, what web browser they’re using, etc. Classifier will predict whether or not the user will make a purchase.

To measure accuracy used two values: sensitivity (“true positive rate”) and specificity (“true negative rate”). Sensitivity refers to the proportion of positive examples that were correctly identified. Specificity refers to the proportion of negative examples that were correctly identified. 


### K Nearest Neighbor(KNN) algorithm

In this project used KNN algorithm from Python [Scikit-learn package](https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KNeighborsClassifier.html).

**KNN** is a popular machine learning algorithm which is used in the variety of applications: healthcare, finance, image recognition, etc. This algorithm used for both classification and regression problems. 

**What is K**? In KNN, K is the number of nearest neighbors. 

**How it works?** If *K*=1. If we have new value *V* which label we want predict. First we find the one closest point to *V* and then the label of this point assign to N.
If *K*>1 we find the *K* closest points to *V*, then classify points by majority vote of its *K* neighbors. Each neighbor votes for it's class and the class with the most votes is taken as prediction.


## Requirements:

```
scikit-learn
```

## Usage:

```
python shopping.py [DATA.csv]
```

## Result:

```
Correct: 4100
Incorrect: 832
True Positive Rate: 38.83%
True Negative Rate: 91.49%
```

*Video on youtube showing result*

[![Shopping - youtube](https://img.youtube.com/vi/VaXkoFzoj7Y/0.jpg)](https://youtu.be/VaXkoFzoj7Y)
