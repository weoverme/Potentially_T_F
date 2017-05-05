from sklearn import svm

#initialise training data
training_data = []

#get support vectors
feature_vector = []

#get indicies of support vectors

#get number of support vectors for each class

X = [[0, 0], [1, 1]]
y = [0, 1]
clf = svm.SVC()
clf.fit(X, y)
clf.predic