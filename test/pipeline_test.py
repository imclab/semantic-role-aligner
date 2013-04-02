# -*- coding: utf-8 -*-
import sys
sys.path.append('/home/gavin/dev/argument_based_entailment')
import unittest
import pipeline


class Test_classifier(unittest.TestCase):

    def setUp(self):
        self.pipeline = pipeline.Entailment_recognizer()
        self.problems = [
        ('The Mets beat the Yankees', 'The Yankees beat the Mets', False),
        ('I ate a tasty sandwich', 'I ate some food', True),

        ]
        self.targets = [t[2] for t in self.problems]
        self.prediction_codes_key = [True, True, 'Unknown', False, False, False, False]

    def runTest(self):
        prediction_codes = []
        prediction_answers = []
        for p, h, entailed in self.problems:
            prediction = self.pipeline.get_entailment(p, h)
            prediction_codes.append(prediction)

        for prediciton in prediction_codes:
            prediction_answers.append(self.prediction_codes_key[prediciton])

        self.assertEqual(prediction_answers, self.targets)


if __name__ == '__main__':
    unittest.main()