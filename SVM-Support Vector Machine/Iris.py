'split the training and test data as 50% + 50%'
# author = Nicolas Anderson, pyton 3, svm with iris dataset
import numpy as np
from sklearn import svm


training = open("iris.data").readlines()[0::2] #odd numbers
testing = open("iris.data").readlines()[1::2] #even numbers

def getData(lines, labeltype):
    t = [list(map(float, i)) for i in [[i for i in i.split(",")][:-1] for i in lines if i.strip()]]
    t_labels = [i.split(",")[-1:][0].strip('\n') for i in lines if i.strip()]
    t_type = [j for i, j in enumerate(t) if t_labels[i] == labeltype]
    return t_type

train_0 = getData(training,"Iris-setosa")
train_1 = getData(training,"Iris-versicolor")
train_2 = getData(training,"Iris-virginica")

test_0 = getData(testing,"Iris-setosa")
test_1 = getData(testing,"Iris-versicolor")
test_2 = getData(testing,"Iris-virginica")


C = 1.0
gamma = 0.5

X = np.array(train_0+train_1+train_2)
Y = np.array([0 for i in train_0] + [1 for j in train_1]+[2 for k in train_2])

#create different functions of svm
svm_linear = svm.SVC(kernel='linear', C=C, gamma=gamma).fit(X, Y)
svm_rbf = svm.SVC(kernel='rbf', C=C, gamma=gamma).fit(X, Y)
svm_sigmoid = svm.SVC(kernel='sigmoid', C=C, gamma=gamma).fit(X, Y)
svm_poly = svm.SVC(kernel= 'poly', C=C, gamma=gamma).fit(X, Y)

def testSVM(svm, zero, one,two):
    numcorrect = 0.
    numwrong = 0.
    for correct, testing in ((0, zero), (1, one),(2,two)):
        for d in testing:
            r = svm.predict(np.reshape(d,(1,-1)))[0]
            if (r == correct):
                numcorrect += 1
            else:
                numwrong += 1
    print("Correct", numcorrect)
    print("Wrong", numwrong)
    print("Accuracy", (numcorrect)/(numcorrect + numwrong))


x=''
print("Linear")
testSVM(svm_linear, test_0, test_1, test_2)
print(x*10)

print("Polynomial")
testSVM(svm_poly, test_0, test_1, test_2)
print(x*10)

print("RBF")
testSVM(svm_rbf, test_0, test_1, test_2)
print(x*10)

print("Sigmoid")
testSVM(svm_sigmoid,test_0, test_1, test_2)