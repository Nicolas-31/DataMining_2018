import numpy as np
from sklearn import svm

training_data = open("iris.data").readlines()[0::2] #odd numbers
test_data = open("iris.data").readlines()[1::2]  #even numbers


def getData(lines, labeltype):
    t = [list(map(float, i)) for i in [[i for i in i.split(",")][:-1] for i in lines if i.strip()]]
    t_labels = [i.split(",")[-1:][0].strip('\n') for i in lines if i.strip()]
    t_type =[j for i, j in enumerate(t) if t_labels[i] == labeltype]
    return t_type

#split both the training and test data into different classes
training_data_0 = getData(training_data,"Iris-setosa")
training_data_1 = getData(training_data,"Iris-versicolor")
training_data_2 = getData(training_data,"Iris-virginica")

test_data_0 = getData(test_data,"Iris-setosa")
test_data_1 = getData(test_data,"Iris-versicolor")
test_data_2 = getData(test_data,"Iris-virginica")

#C and gamma are constants
C = 1.0
gamma = 0.5

X = np.array(training_data_0 + training_data_1+ training_data_2)
Y = np.array ([0 for i in training_data_0] +[1 for i in training_data_1] +[2 for i in training_data_2])

# create different functions of svm
svm_linear = svm.SVC(kernel='linear', C=C, gamma=gamma).fit(X,Y)
svm_rbf = svm.SVC(kernel='rbf', C=C, gamma=gamma).fit(X,Y)
svm_sigmoid = svm.SVC(kernel='sigmoid', C=C, gamma=gamma).fit(X,Y)
svm_poly = svm.SVC(kernel='poly', C=C, gamma=gamma).fit(X,Y)

def testSVM(svm, zero, one, two):
    numcorrect = 0.
    numwrong = 0.
    for correct, test_data in ((0,zero), (1,one), (2,two)):
        for d in test_data:
            r = svm.predict(np.reshape(d,(1,-1)))[0]
            if (r == correct):
                numcorrect += 1
            else:
                numwrong += 1
    print("Correct", numcorrect)
    print("Wrong", numwrong)
    print("Accuracy",(numcorrect)/(numcorrect + numwrong))


x = ''
print("Linear")
testSVM(svm_linear, test_data_0, test_data_1, test_data_2)
print(x*10)

print("Polynomial")
testSVM(svm_poly, test_data_0, test_data_1, test_data_2)
print(x*10)


print("RBF")
testSVM(svm_rbf, test_data_0, test_data_1, test_data_2)
print(x*10)

print("Sigmoid")
testSVM(svm_sigmoid, test_data_0, test_data_1, test_data_2)
print(x*10)