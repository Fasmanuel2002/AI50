import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
import random
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
    with open(filename ,'r') as f1:
        reader = csv.reader(f1)
        next(reader)
        evidence = []
        label = []
        for row in reader:
            evidence.append([
                int(row[0]),
                float(row[1]),
                int(row[2]),
                float(row[3]),
                int(row[4]),
                float(row[5]),
                float(row[6]),
                float(row[7]),
                float(row[8]),
                float(row[9]),
                0 if row[10] == "Jan" else 1 if row[10] == "Feb" else 2 if row[10] == "Mar"
                else 3 if row[10] == "Apr" else 4 if row[10] == "May" else 5 if row[10] == "Jun"
                else 6 if row[10] == "Jul" else 7 if row[10] == "Aug" else 8 if row[10] == "Sep"
                else 9 if row[10] == "Oct" else 10 if row[10] == "Nov" else 11,
                int(row[11]),
                int(row[12]),
                int(row[13]),
                int(row[14]),
                1 if row[15] == "Returning_Visitor" else 0,
                1 if row[16] == "TRUE" else 0
            ])
            label.append([1 if row[17] == "TRUE" else 0])

        return(evidence, label)
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



def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(1)
    model.fit(evidence,labels)
    return(model)

def evaluate(labels, predictions):
    #labels (the true labels for the users in the testing set) and a list of predictions (the labels predicted by your classifier)


    sensitivity = 0
    specificity = 0
    TrueNegatives = 0
    FalsePositives = 0
    TruePositives = 0
    FalseNegatives = 0
    for actual, predicition in zip(labels,predictions):
        if actual == 1 and predicition == 1:
            TruePositives += 1
        elif actual == 1 and predicition == 0:
            FalseNegatives +=1
        elif actual == 0 and predicition == 1:
            TrueNegatives += 1
        elif actual == 0 and predicition == 0:
            FalsePositives += 1


    sensitivity = TruePositives /(TruePositives + FalseNegatives)
    specificity = TrueNegatives/(TrueNegatives + FalsePositives)
    return (sensitivity, specificity)
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).


    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """


if __name__ == "__main__":
    main()
