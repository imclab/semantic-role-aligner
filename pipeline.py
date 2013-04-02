# -*- coding: utf-8 -*-
'''
This really is an entailer with semantic role representation

inputs:
    p string
    h string

do:
    p roles = getPRoles(p string)
    h roles = getHRoles(h string)

    aligned_role_entailments = []
    for p_role in p roles:
        for h_role in h roles:
            getFeatureVector(p_role, h_role)
            p_symmetric = getVerbSymmetry(p_role)
            h_symmetry = getVerbSymmetry(h_role)
            if p_symmetric and/or? h_symmetric:
                acceptance_prediction = classifySymmetricAcceptance(p_role, h_role)
            else:
                acceptance_prediction = classifyAsymmetricAcceptance(p_role, h_role)
            if acceptance_prediction == accepted:
                entailment = getEntailment(p_role, h_role)
                aligned_role_entailments.append(entailment)

    entailment = join_entailments(aligned_role_entailments)
    return entailment

'''
import senna_interface
import phrase_alignment_featurizer as paf
import entailment_joiner
from acceptance_classifiers import classifier_asym
from acceptance_classifiers import classifier_sym
import entailment_interface as eai


class Entailment_recognizer(object):

    def __init__(self):
        self.senna_interface = senna_interface.Senna_interface()
        self.featurizer = paf.Phrase_alignment_featurizer()
        self.classifier_asym = classifier_asym.Classifier_asym()
        self.classifier_sym = classifier_sym.Classifier_sym()
        self.entailment_API = eai.Entailment_API_interface()
        self.joiner = entailment_joiner.Entailment_joiner()

    def get_entailment(self, p, h):
        print 'P:\n', p
        print 'H:\n', h
        p_roles, p_is_symmetric = self.senna_interface.get_semantic_roles(p)
        h_roles, h_is_symmetric = self.senna_interface.get_semantic_roles(h)
        print 'P is symmetric:', p_is_symmetric
        print 'H is symmetric:', h_is_symmetric
        print '\n\n'
        aligned_role_entailments = []
        for i in p_roles:
            print 'p role:', i

        print '\n'
        for i in h_roles:
            print 'h role:', i
        print '\n\n\n'

        del_roles = p_roles[:]
        ins_roles = h_roles[:]

        print 'del roles'
        for i in del_roles:
            print i

        print '\n\n'
        print 'ins roles'
        for i in ins_roles:
            print i

        for p_role in p_roles:
            for h_role in h_roles:
                print '\n\nP role:\n', p_role
                print 'H role:\n', h_role
                features = self.featurizer.featurize(p_role, h_role)
                print 'Feature vector:\n', features
                if p_is_symmetric and h_is_symmetric:
                    print 'using symmetric classifier'
                    acceptance = self.classifier_sym.classify(features)
                else:
                    print 'using asymmetric classifier'
                    acceptance = self.classifier_asym.classify(features)[0]
                print 'Accepted:', acceptance
                if acceptance == 1:
                    print 'removing role'
                    del_roles.remove(p_role)
                    ins_roles.remove(h_role)
                    entailment = self.entailment_API.get_entailment(p_role, h_role)
                    print 'Predicted entailment:', entailment
                    aligned_role_entailments.append(entailment)
                else:
                    pass
                    # handle INS/DEL for roles individually?
                    # Not yet; role might be aligned to something else.


        print 'del roles'
        for i in del_roles:
            print i

        print '\n\n'
        print 'ins roles'
        for i in ins_roles:
            print i

        # At the end, find the roles that were not aligned to anything
        # Then need to do monotonicity and projection
        entailment = self.joiner.join(aligned_role_entailments)
        print 'Joined entailment:', entailment
        return entailment

if __name__ == '__main__':
    #p = 'Carolina beat Kansas.'
    #h = 'Carolina defeated Kansas.'
    #h = 'Kansas beat Carolina.'
    p = 'I ate a pizza.'
    h = 'I ate food.'
    recognizer = Entailment_recognizer()
    entailment = recognizer.get_entailment(p, h)