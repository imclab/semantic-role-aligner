# -*- coding: utf-8 -*-
"""
Created on 20130325

@author: gavinhackeling@gmail.com

/senna-linux64 -posvbs <<< 'I ate a cake.'

"""
from subprocess import Popen, PIPE, STDOUT
from model import semantic_role as sr


class Senna_interface(object):

    def __init__(self):
        pass

    def get_semantic_roles(self, text_str):
        pipe = Popen([
            '/home/gavin/dev/senna/senna2',
            '-posvbs'],
            cwd='/home/gavin/dev/senna',
            stdout=PIPE, stdin=PIPE, stderr=STDOUT)
        out = pipe.communicate(input='%s' % text_str)[0]
        out_lines = out.split('\n')
        #for i in out_lines:
            #print 'line:', i
            #if i == '\n':
                #print 'foudn one'
        #print '\n\n\n'
        out_lines = [l for l in out_lines if 1 != '\n']
        tokens = out_lines[0].split('\t')[1:]
        pos_tags = out_lines[1].split('\t')[1:]
        chunk_tags = out_lines[2].split('\t')[1:]
        ne_labels = out_lines[3].split('\t')[1:]
        predicate_labels = out_lines[4].split('\t')[1:]
        # TODO
        # There may be multiple verbs in the sentence; each will have its own
        # arguments. semantic_role_labels only contains the chunk tags for the
        # first (and hopefully main) verb's arguments
        semantic_role_labels = out_lines[5].split('\t')[1:]
        #print 'tokens', tokens
        #print 'pos tags', pos_tags
        #print 'chunk tags', chunk_tags
        #print 'ne labels', ne_labels
        #print 'predicate labels', predicate_labels
        #print 'semantic role labels', semantic_role_labels

        semantic_roles = []
        for i, label in enumerate(semantic_role_labels):
            if label[0] == 'S':
                phrase_indices = []
                role = sr.Semantic_role(
                    [tokens[i]], pos_tags[i], chunk_tags[i],
                    ne_labels[i], predicate_labels[i], [semantic_role_labels[i]]
                )
                semantic_roles.append(role)
            elif label[0] == 'B':
                phrase_indices = [i]
            elif label[0] == 'E':
                phrase_indices.append(i+1)
                role = sr.Semantic_role(
                    tokens[phrase_indices[0]:phrase_indices[1]],
                    pos_tags[phrase_indices[0]:phrase_indices[1]],
                    chunk_tags[phrase_indices[0]:phrase_indices[1]],
                    ne_labels[phrase_indices[0]:phrase_indices[1]],
                    predicate_labels[phrase_indices[0]:phrase_indices[1]],
                    semantic_role_labels[phrase_indices[0]:phrase_indices[1]]
                )
                semantic_roles.append(role)
            elif label[0] == 'O':
                phrase_indices = []
                semantic_roles.append(sr.Semantic_role(
                    [tokens[i]], pos_tags[i], chunk_tags[i],
                    ne_labels[i], predicate_labels[i], [semantic_role_labels[i]]
                ))

        return semantic_roles


if __name__ == '__main__':
    si = Senna_interface()
    roles = si.get_semantic_roles('Pope Francis will continue to use the papal library on the second floor of the Apostolic palace for receiving official guests and will appear on Sundays at the window used by previous popes to address pilgrims in St Peters Square.')
    for i in roles:
        print i