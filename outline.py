# -*- coding: utf-8 -*-
'''
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