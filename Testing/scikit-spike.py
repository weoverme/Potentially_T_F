from sklearn import svm
from Testing.dataset_maker import *
import numpy as np


#initialise training data
training_data = TrainingData()
training_data.retrieve()

print(training_data.data.shape)

X = numpy.ndarray(training_data.data)
print(training_data.data.shape)

#X = X.reshape(1, -1)

y = training_data.target
clf = svm.SVC(gamma=0.01)
clf.fit(X, y)
#clf.reshape(1, -1)

text1 = "You must get it for our future."
text2 = "In order to obtain the paper, we must first buy the paper"
pos = pos_tag(word_tokenize(text1))

# save all features into featureList
postag_tokens_of_tweet = []
for token in pos:
    feat = token[1]
    if feat not in postag_tokens_of_tweet:
        postag_tokens_of_tweet.append(token)

test = get_sample_feature_vectors(postag_tokens_of_tweet, training_data)
print(test)
print("Expected: -1\tActual:", clf.predict(test))