# -*- coding: utf-8 -*-
'''
Compose an entailment relation by joining a list of atomic entailment relations.
'''
import numpy as np


class Entailment_joiner(object):

    def __init__(self):
        self.join_table = np.array([
            [0, 1, 2, 3, 4, 5, 6],
            [1, 1, 6, 4, 4, 6, 6],
            [2, 6, 2, 5, 6, 5, 6],
            [3, 5, 4, 0, 2, 1, 6],
            [4, 6, 4, 1, 6, 1, 6],
            [5, 5, 6, 2, 2, 6, 6],
            [6, 6, 6, 6, 6, 6, 6],
        ], dtype=np.uint)

    def join(self, entailments):
        '''
        Given a list of atomic entailment relations,
        compose an entailment relation for the sequence.
        '''
        previous_composition = 0
        for i in entailments:
            print 'joining', type(i), i
            previous_composition = self.join_table[previous_composition][int(i)]
        return previous_composition

if __name__ == '__main__':
    joiner = Entailment_joiner()
    print joiner.join([1, 1, 1, 0, 1])
