# -*- coding: utf-8 -*-
"""
Created on 20130325

@author: gavin
"""
from nltk.corpus import wordnet as wn


class Sub:

    def __init__(self,
        p_tokens, p_lemmas, p_penn_tags,
        h_tokens, h_lemmas, h_penn_tags):

        self.tag_conversion_dict = {
            'NN': wn.NOUN, 'JJ': wn.ADJ, 'VB': wn.VERB, 'RB': wn.ADV
        }
        self.p_tokens = p_token
        self.p_lemmas = p_lemma
        self.p_penn_tags = p_penn_tag
        self.p_wn_tags = self.get_wn_tags(self.p_penn_tags)
        self.h_tokens = h_token
        self.h_lemmas = h_lemma
        self.h_penn_tags = h_penn_tag
        self.h_wn_tags = self.get_wn_tags(self.h_penn_tags)
        self.lexical_entailment = 'NONE'
        self.monotonicity = 'NONE'

    def get_wn_tags(self, penn_tags):
        wn_tags = []
        for penn_tag in penn_tags:
            if penn_tag[:2] in self.tag_conversion_dict.keys():
                wn_tags.append(self.tag_conversion_dict[penn_tag[:2]])
            else:
                wn_tags.append('SKIP')
        return wn_tags

    def __repr__(self):
        return '''
            SUB\n
            p_tokens: %s\n
            h_tokens: %s\n
            p_pos_tags: %s\n
            h_pos_tags: %s\n
            Monotonicity: %s\n
            Lexent: %s\n''' % (
            ', '.join([t.encode('utf-8', 'ignore') for t in self.p_tokens]),
            ', '.join([t.encode('utf-8', 'ignore') for t in self.h_tokens]),
            ', '.join([t.encode('utf-8', 'ignore') for t in self.p_penn_tags]),
            ', '.join([t.encode('utf-8', 'ignore') for t in self.h_penn_tags]),
            self.monotonicity,
            self.lexical_entailment
        )

