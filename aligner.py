# -*- coding: utf-8 -*-
"""

"""
import phrase_alignment_featurizer as paf
import senna_interface


class Aligner(object):

    def __init__(self):
        self.si = senna_interface.Senna_interface()
        self.alignment_featurizer = paf.Phrase_alignment_featurizer()

    def get_phrases(self, p, h):
        '''
        Get the arguments and predicates for a sentence from SENNA
        '''
        p_phrases = self.si.get_semantic_roles(p)
        h_phrases = self.si.get_semantic_roles(h)
        print 'p phrases:'
        for i in p_phrases:
            print i
            print i.get_arg_type()
        print 'h phrases:'
        for i in h_phrases:
            print i
            print i.get_arg_type()
        return p_phrases, h_phrases

    def get_featurized_phrases_alignments(self, p_phrases, h_phrases):
        '''
        Get a feature vector for each phrase alignment in the cartesian product
        of p phrases and h phrases
        '''
        featurized_alignments = []
        h_test = ' '.join(h_phrases[0].tokens)
        for p_phrase in p_phrases:
            #print p_phrase.tokens, len(p_phrase.tokens)
            if len(p_phrase.tokens) > 1:
                p_str = ' '.join(p_phrase.tokens)
            else:
                p_str = p_phrase.tokens[0]
            #print '*p_str:', p_str
            for h_phrase in h_phrases:
                if len(h_phrase.tokens) > 1:
                    h_str = ' '.join(h_phrase.tokens)
                else:
                    h_str = h_phrase.tokens[0]
                #print '**h str:', h_str
                score = self.alignment_featurizer.featurize_phrase_alignment(
                    p_str, h_str)
                #print 'score for', p_str, h_str, score
                featurized_alignments.append((score, p_str, h_str))
        return featurized_alignments

    def classify_phrase_alignments(self, featurized_alignments):
        '''
        Given a feature vector, classify whether or not the alignment shoud be
        accepted.
        '''
        classified_alignments = []

        return classified_alignments

if __name__ == '__main__':
    p = "Barack Obama, the first black president, went to Harvard."
    h = "Barack Obama was the first black president."
    #h = """Pope Francis will continue to use the papal library on the second floor of the Apostolic palace for receiving official guests and will appear on Sundays at the window used by previous popes to address pilgrims in St Peters Square."""
    aligner = Aligner()
    p_phrases, h_phrases = aligner.get_phrases(p, h)
    featurized_alignments = aligner.get_featurized_phrases_alignments(
        p_phrases, h_phrases)
    #for i in featurized_alignments:
        #print i
    classified_alignments = aligner.classify_phrase_alignments(
        featurized_alignments)
