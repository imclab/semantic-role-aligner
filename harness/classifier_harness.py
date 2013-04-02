# -*- coding: utf-8 -*-
'''
Read training problem json

Use phrase alignment featurizer to get feature vector

fit classifier (random forest)

pickle model
'''
import sys
sys.path.append('/home/gavin/dev/argument_based_entailment')
import os
import json
from time import time
try:
    import cPickle as pickle
except:
    import pickle  # lint:ok
import numpy as np
from nltk import word_tokenize, pos_tag, ne_chunk
import phrase_alignment_featurizer as paf
from model import semantic_role


class Harness(object):

    def __init__(self):
        filename = os.path.join(os.path.dirname(__file__),
        '../resources/training_data/phrase_alignment_training.json')
        with open(filename) as f:
            raw_json = f.read()
        self.problems = json.loads(raw_json)
        self.featurizer = paf.Phrase_alignment_featurizer()

        features = []
        targets_asym = []
        targets_sym = []
        start = time()
        for index, problem in enumerate(self.problems):
            print 'Starting problem', index
            tokens = word_tokenize(problem['p'])
            pos_tagged_tokens = pos_tag(tokens)
            chunks = ne_chunk(pos_tagged_tokens)
            ne_labels = problem['p_ne']
            arg_type = problem['p_arg']
            p_role = semantic_role.Semantic_role(
                tokens, pos_tagged_tokens, chunks, ne_labels, arg_type)
            #print p_role

            tokens = word_tokenize(problem['h'])
            pos_tagged_tokens = pos_tag(tokens)
            chunks = ne_chunk(pos_tagged_tokens)
            ne_labels = problem['h_ne']
            arg_type = problem['h_arg']
            h_role = semantic_role.Semantic_role(
                tokens, pos_tagged_tokens, chunks, ne_labels, arg_type)
            #print h_role

            feature_vector = self.featurizer.featurize(p_role, h_role)
            features.append(feature_vector)
            targets_asym.append(problem['aligned_asym'])
            targets_sym.append(problem['aligned_sym'])

        feature_vectors_matrix = np.vstack(features)
        # Write the feature vectors
        features_file = open(
            '../resources/models/phrase_alignment_features.p', 'w+b')
        pickle.dump(feature_vectors_matrix, features_file)
        features_file.close()
        # Write the asym targets
        targets_asym_file = open(
            '../resources/models/phrase_alignment_targets_asym.p', 'w+b')
        pickle.dump(targets_asym, targets_asym_file)
        targets_asym_file.close()
        # Write the sym targets
        targets_sym_file = open(
            '../resources/models/phrase_alignment_targets_sym.p', 'w+b')
        pickle.dump(targets_sym, targets_sym_file)
        targets_sym_file.close()

        print targets_asym
        print '\n\n\n', targets_sym

        print len(self.problems)
        print len(targets_asym)
        print len(targets_sym)
        print len(features)
        print 'Trained with %s problems in %s seconds' % (
            len(self.problems), time()-start)

if __name__ =='__main__':
    harness = Harness()