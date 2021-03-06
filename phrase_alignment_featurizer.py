# -*- coding: utf-8 -*-
"""

Score an alignment of two phrases (arguments or predicates).
Accept the alignment if the score exceeds a threshold.
Use an SVM or tree on a feature vector instead, trained on examples
need to make 2-label training data:
    align? yes or no

This is a simple representation that permits any phrase to be aligned to zero
or more phrases.

The following similarity measures are used:
    -token alignment features
    -matching V
    -matching A0
    -matching AN, N>0
"""
from json import load
from urllib import urlopen, urlencode
import urllib2
import numpy as np
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet as wn
from model import semantic_role
import simplejson
import json


class Phrase_alignment_featurizer(object):

    def __init__(self):
        self.base_url = 'http://localhost:8000/align/string?'

    def have_AN_match(self, p_arg_type, h_arg_type):
        '''
        If both of the roles are arguments and they have the same index return 1
        '''
        if p_arg_type == h_arg_type:
            if p_arg_type[0] == 'A':
                #print '%s and %s match each other' % (p_arg_type, h_arg_type)
                return 1
        #print 'No AN match'
        return 0

    def have_AN_greater_match(self, p_arg_type, h_arg_type):
        '''
        If both of the roles are arguments return 1
        '''
        #print p_arg_type, h_arg_type
        if p_arg_type[0] == h_arg_type[0] == 'A':
            #print '%s and %s match AN' % (p_arg_type, h_arg_type)
            return 1
        #print 'No AN Greater match'
        return 0

    def have_A0_A1_mismatch(self, p_arg_type, h_arg_type):
        '''
        If one role has type A0 and the other has type A1, return 1
        '''
        #print '***', p_arg_type, h_arg_type
        if p_arg_type == 'A0' and h_arg_type == 'A1':
            #print '%s mismatches %s' % (p_arg_type, h_arg_type)
            return 1
        elif p_arg_type == 'A1' and h_arg_type == 'A0':
            #print '%s mismatches %s' % (p_arg_type, h_arg_type)
            return 1
        #print 'No A0 A1 mismatch'
        return 0

    def have_V_match(self, p_arg_type, h_arg_type):
        '''
        If both of the roles are verbs return 1
        '''
        if p_arg_type == h_arg_type == 'V':
            #print '%s and %s match V' % (p_arg_type, h_arg_type)
            return 1
        #print 'No V match'
        return 0

    def have_AM_match(self, p, h):
        '''
        If both the roles are the same type of ?discourse marker? return 1
        '''
        #if :
            #return 1
        return 0

    def featurize(self, p, h):
        '''
        Return a vector of lexical and role type features for a pair of roles
        '''
        p_str = ' '.join(p.tokens)
        h_str = ' '.join(h.tokens)
        arg_features = np.zeros(5)
        parameters = {
            "p": p_str,
            "h": h_str,
            "w": 'default'
        }
        query_string = urlencode(parameters)
        url = self.base_url + query_string
        #print url
        response = urllib2.urlopen(url)
        result_str = response.read()
        result_json = simplejson.loads(result_str)
        lex_features = result_json['averaged_features']

        p_arg_type = p.get_arg_type()
        h_arg_type = h.get_arg_type()
        #print 'p arg', p_arg_type
        #print 'h arg', h_arg_type
        arg_features[0] = self.have_AN_match(p_arg_type, h_arg_type)
        arg_features[1] = self.have_AN_greater_match(p_arg_type, h_arg_type)
        arg_features[2] = self.have_A0_A1_mismatch(p_arg_type, h_arg_type)
        arg_features[3] = self.have_V_match(p_arg_type, h_arg_type)
        #arg_features[4] = self.have_AM_match(p_arg_type, h_arg_type)
        arg_features[4] = 0

        features = np.concatenate([arg_features, lex_features])
        #print 'features for:', '\n', p, '\n', h, '\n', features, '\n'
        return features

if __name__ == '__main__':
    featurizer = Phrase_alignment_featurizer()
    #p = semantic_role.Semantic_role(
        #'jump', 'VB', 'VP', None, 'V'
    #)
    #h = semantic_role.Semantic_role(
        #'leap', 'VB', 'VP', None, 'V'
    #)
    #p = semantic_role.Semantic_role(
        #'jump', 0, 'VB', 'VP', None, 'A0'
    #)
    #h = semantic_role.Semantic_role(
        #'jump', 0, 'VB', 'VP', None, 'A1'
    #)
    #p = semantic_role.Semantic_role(
        #['A', 'dog'], '', 'VP', None, 'A0'
    #)
    #h = semantic_role.Semantic_role(
        #'leap', 'VB', 'VP', None, 'A0'
    #)
    p = semantic_role.Semantic_role(
        ['a', 'tasty', 'sandwich'],
        [0, 1, 2],
        ['DT', 'JJ', 'NN'],
        ['B-NP', 'I-NP', 'E-NP'],
        None,
        'A1'
    )
    h = semantic_role.Semantic_role(
        ['some', 'food'],
        [0, 1],
        ['DT', 'NN'],
        ['B-NP', 'E-NP'],
        None,
        'A1'
    )
    print featurizer.featurize(p, h)

    p = semantic_role.Semantic_role(
        ['a', 'tasty', 'sandwich'],
        [0, 1, 2],
        ['DT', 'JJ', 'NN'],
        ['B-NP', 'I-NP', 'E-NP'],
        None,
        'A1'
    )
    h = semantic_role.Semantic_role(
        ['cat', 'hats'],
        [0, 1],
        ['NN', 'NNS'],
        ['B-NP', 'E-NP'],
        None,
        'A1'
    )
    print featurizer.featurize(p, h)
