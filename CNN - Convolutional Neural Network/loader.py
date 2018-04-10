import numpy as np
from PIL import Image
import pickle

def openFile(filename, skip=True):
    with open(filename, 'r') as f: #
        if skip:
            f.readline()
        return f.readlines()


def getPathName(a, b, c):
    return 'lfw/' + str(a[b]) + '/' + str(a[b]) + '_' + str(str(c).zfill(4)) + '.jpg'


def getImgage(path):
    image = Image.open(path).crop((5, 5, 245, 245)).resize((80, 80))
    return np.asarray(image, dtype="uint8")

def getDataSet(filename):
    x, y = ([], [])

    for line in openFile(filename):
        l = line.split()
        if l[0] in open('female_names.txt').read():
        #if l[0] in open('male_names.txt').read():
            label = 1
        else:
            label = 0
        for i in range(int(l[1])):
            path = getPathName(l, 0, i+1)
            x.append(getImgage(path))
            y.append(label)
    return x, y


x = getDataSet('peopleDevTrain.txt')
y = getDataSet('peopleDevTest.txt')
pickle.dump((x, y), open('female.p', 'wb'))
#pickle.dump((x, y), open('male.p', 'wb'))