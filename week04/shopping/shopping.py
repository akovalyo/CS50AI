import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

from sklearn import metrics

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """

    with open(filename, encoding="utf-8") as csvf:
        reader = csv.reader(csvf)
        next(reader)
        evidence = []
        labels = []
        month = {'Jan': 0, 'Feb': 1, 'Mar': 2, 'Apr': 3, 'May': 4, 'June': 5,
                 'Jul': 6, 'Aug': 7, 'Sep': 8, 'Oct': 9, 'Nov': 10, 'Dec': 11}
        for row in reader:
            evid_one = []
            evid_one.append(int(row.pop(0)))
            evid_one.append(float(row.pop(0)))
            evid_one.append(int(row.pop(0)))
            evid_one.append(float(row.pop(0)))
            evid_one.append(int(row.pop(0)))
            evid_one.append(float(row.pop(0)))
            evid_one.append(float(row.pop(0)))
            evid_one.append(float(row.pop(0)))
            evid_one.append(float(row.pop(0)))
            evid_one.append(float(row.pop(0)))
            evid_one.append(month[row.pop(0)])
            evid_one.append(int(row.pop(0)))
            evid_one.append(int(row.pop(0)))
            evid_one.append(int(row.pop(0)))
            evid_one.append(int(row.pop(0)))
            tmp = row.pop(0)
            evid_one.append(0 if tmp == 'New_Visitor' else 1)
            tmp = row.pop(0)
            evid_one.append(0 if tmp == 'FALSE' else 1)
            tmp = row.pop(0)
            labels.append(0 if tmp == 'FALSE' else 1)
            evidence.append(evid_one)
        return (evidence, labels)
            

def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    
    model = KNeighborsClassifier(n_neighbors=1)
    model.fit(evidence, labels)
    print(model)
    return model


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificty).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    
    pos_predict = 0
    neg_predict = 0
    pos_labels = 0
    neg_labels = 0
    sensitivity = 0.0
    specificity = 0.0

    for l, p in zip(labels, predictions):
        if l == 1:
            pos_labels += 1
            if l == p:
                pos_predict += 1
        elif l == 0:
            neg_labels += 1
            if l == p:
                neg_predict += 1
    
    sensitivity = pos_predict / pos_labels
    specificity = neg_predict / neg_labels 
    print(sensitivity, specificity)
    return (sensitivity, specificity)


if __name__ == "__main__":
    main()
