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
from model import semantic_role as sr


class Entailment_recognizer(object):

    def __init__(self):
        self.senna_interface = senna_interface.Senna_interface()
        self.featurizer = paf.Phrase_alignment_featurizer()
        self.classifier_asym = classifier_asym.Classifier_asym()
        self.classifier_sym = classifier_sym.Classifier_sym()
        self.entailment_API = eai.Entailment_API_interface()
        self.joiner = entailment_joiner.Entailment_joiner()

    def get_entailment(self, p, h):
        # For the p and h strings, get whether the verb is symmetric and
        # its list of predicates and arguments
        p_roles, p_is_symmetric = self.senna_interface.get_semantic_roles(p)
        h_roles, h_is_symmetric = self.senna_interface.get_semantic_roles(h)
        # For making lists of roles that were not aligned
        del_roles = p_roles[:]
        ins_roles = h_roles[:]
        aligned_role_entailments = []

        # TODO Must mark monotonicities before entailer.
        # DONE Entailer should not mark
        # DONE add parameter to entailer API that sets monotonicity marker on or off monotonicities.

        # TODO If monotone markers are found in p or h
        # TODO Mark the monotonicity of each token/index
        # TODO Check each role if it contains the token/index and add the markings

        print 'P (symmetric: %s): %s' % (p_is_symmetric, p)
        print 'H (symmetric: %s): %s' % (h_is_symmetric, h)
        print '\n'
        for i in p_roles:
            print 'p role:', i, '\n'
        print '\n'
        for i in h_roles:
            print 'h role:', i, '\n'
        print '\n'

        # Align roles from p to roles from h
        for p_role in p_roles:
            for h_role in h_roles:
                print '\nP role:', p_role.tokens
                print 'H role:', h_role.tokens
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
                    #print 'removing role'
                    del_roles.remove(p_role)
                    ins_roles.remove(h_role)
                    entailment = self.entailment_API.get_sub_entailment(p_role, h_role)
                    print 'Predicted entailment:', entailment
                    aligned_role_entailments.append((
                        'SUB', entailment, (p_role.tokens, h_role.tokens)))
                else:
                    pass
                    # handle INS/DEL for roles individually?
                    # Not yet; role might be aligned to something else.

        # Get entailments for DELeted roles
        for del_role in del_roles:
            entailment = self.entailment_API.get_del_entailment(del_role)
            aligned_role_entailments.append((
                'DEL', entailment, (del_role.tokens)))

        # Get entailments for INSerted roles
        for ins_role in ins_roles:
            entailment = self.entailment_API.get_ins_entailment(ins_role)
            aligned_role_entailments.append((
                'INS', entailment, (ins_role.tokens)))

        # Print role alignment type, entailment, and tokens
        print 'aligned roles'
        for i in aligned_role_entailments:
            print i

        # Join the entailments for the role alignments
        entailment = self.joiner.join(
            [e for ty, e, to in aligned_role_entailments])
        print 'Joined entailment:', entailment
        return entailment

if __name__ == '__main__':
    p = 'Carolina beat Kansas.'
    h = 'Carolina defeated Kansas.'
    #h = 'Kansas beat Carolina.'
    #p = 'at the zoo I ate a pizza.'
    #h = 'I ate food on Tuesday.'
    recognizer = Entailment_recognizer()
    entailment = recognizer.get_entailment(p, h)