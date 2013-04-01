# -*- coding: utf-8 -*-
'''

'''
import sys
import unittest
sys.path.append('/home/gavin/dev/phrase_aligner')
from harness import training_parser
from acceptance_classifiers import classifier_sym


class Test_classifier(unittest.TestCase):

    def setUp(self):
        self.clf = classifier_sym.Classifier_sym()
        self.training_parser = training_parser.Training_parser()

    def runTest(self):
        feature_vectors, targets_asym, targets_sym = self.training_parser.parse('phrase_alignment_test.json')
        predictions = []
        for feature_vector in feature_vectors:
            predictions.append(self.clf.predict(feature_vector))
        self.assertEqual(predictions, targets_sym)


if __name__ == '__main__':
    unittest.main()
