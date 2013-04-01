# -*- coding: utf-8 -*-
'''

'''
import os
import json
from nltk import word_tokenize, pos_tag, ne_chunk
import phrase_alignment_featurizer as paf
from model import semantic_role


class Training_parser(object):

    def __init__(self):
        self.base_path = '/home/gavin/dev/phrase_aligner/resources/training_data'

    def parse(self, path):
        file_name = os.path.join(self.base_path, path)
        print file_name
        with open(file_name) as f:
            raw_json = f.read()
        print raw_json
        self.problems = json.loads(raw_json)
        self.featurizer = paf.Phrase_alignment_featurizer()

        features = []
        targets_asym = []
        targets_sym = []
        for index, problem in enumerate(self.problems):
            print 'Adding problem', index
            tokens = word_tokenize(problem['p'])
            pos_tagged_tokens = pos_tag(tokens)
            chunks = ne_chunk(pos_tagged_tokens)
            ne_labels = problem['p_ne']
            arg_type = problem['p_arg']
            p_role = semantic_role.Semantic_role(
                tokens, pos_tagged_tokens, chunks, ne_labels, arg_type)

            tokens = word_tokenize(problem['h'])
            pos_tagged_tokens = pos_tag(tokens)
            chunks = ne_chunk(pos_tagged_tokens)
            ne_labels = problem['h_ne']
            arg_type = problem['h_arg']
            h_role = semantic_role.Semantic_role(
                tokens, pos_tagged_tokens, chunks, ne_labels, arg_type)

            feature_vector = self.featurizer.featurize(p_role, h_role)
            features.append(feature_vector)
            targets_asym.append(problem['aligned_asym'])
            targets_sym.append(problem['aligned_sym'])

        return features, targets_asym, targets_sym
