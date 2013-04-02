# -*- coding: utf-8 -*-
'''
A random forest classifier for predicting whether a pair of semantic roles
should be aligned.
'''
import os
try:
    import cPickle as pickle
except:
    import pickle  # lint:ok

from sklearn.ensemble import RandomForestClassifier


class Classifier_sym:

    def __init__(self):
        base_path = '/home/gavin/dev/argument_based_entailment/resources/models'
        model_path = os.path.join(
            base_path, 'phrase_alignment_features.p')
        training_file = open(model_path)
        training_data = pickle.load(training_file)
        training_file.close()

        targets_path = os.path.join(base_path, 'phrase_alignment_targets_sym.p')
        targets_file = open(targets_path)
        targets = pickle.load(targets_file)
        targets_file.close()

        self.clf = RandomForestClassifier()
        self.clf = self.clf.fit(training_data, targets)

    def classify(self, feature_vector):
        return self.clf.predict(feature_vector)

if __name__ == '__main__':
    clf = Classifier_sym()
    print clf.classify([1.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 1.0, 0.0975, 0.0975, 0.0, 0.0, 0.0, 0.0, 0.095, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0])