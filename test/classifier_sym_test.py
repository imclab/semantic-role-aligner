# -*- coding: utf-8 -*-
'''

'''
import sys
import unittest
sys.path.append('/home/gavin/dev/argument_based_entailment')
from harness import training_parser
from acceptance_classifiers import classifier_sym


class Test_classifier(unittest.TestCase):

    def setUp(self):
        self.clf = classifier_sym.Classifier_sym()
        self.training_parser = training_parser.Training_parser()

    def runTest(self):
        feature_vectors, targets_sym, targets_sym = self.training_parser.parse('phrase_alignment_test.json')
        predictions = []
        for feature_vector in feature_vectors:
            predictions.append(self.clf.classify(feature_vector)[0])
        print 'targets\n', targets_sym
        print 'predictions\n', predictions
        correct = 0
        incorrect = 0
        for index, value in enumerate(targets_sym):
            if value == predictions[index]:
                correct += 1
            else:
                incorrect += 1
                print 'failed problem', index, 'target', value, 'prediction', predictions[index]
        print 'correct', correct
        print 'incorrect', incorrect
        print 'total', len(predictions)
        self.assertEqual(predictions, targets_sym)


if __name__ == '__main__':
    unittest.main()
