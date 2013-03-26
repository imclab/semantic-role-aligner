# -*- coding: utf-8 -*-
"""

"""
import senna_interface


class Aligner(object):

    def __init__(self):
        self.si = senna_interface.Senna_interface()

    def go(self):
        p = "Barack Obama, the first black president, went to Harvard."
        h = "Barack Obama was the first black president."
        p_phrases = self.si.get_semantic_roles(p)
        h_phrases = self.si.get_semantic_roles(h)

        print 'p phrases:'
        for i in p_phrases:
            print i
        print 'h phrases:'
        for i in h_phrases:
            print i


if __name__ == '__main__':
    aligner = Aligner()
    aligner.go()