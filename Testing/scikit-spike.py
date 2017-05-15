from sklearn import svm
from Main.dataset import *

#initialise training data


#get support vectors
feature_vector = []

#get indicies of support vectors

#get number of support vectors for each class

X = [[0, 0], [1, 1]]
y = [0, 1]
clf = svm.SVC()
clf.fit(X, y)
clf.predict([0,0])