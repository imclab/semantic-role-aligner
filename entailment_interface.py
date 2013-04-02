# -*- coding: utf-8 -*-
'''
http://localhost:8001/e?p=i%20ate%20pizza&h=i%20ate%20food
'''
from json import load
from urllib import urlopen
from urllib import urlencode


class Entailment_API_interface(object):

    def __init__(self):
        self.base_url = 'http://localhost:8001/e?'

    def get_entailment(self, p_role, h_role):
        p_str = ' '.join(p_role.tokens)
        h_str = ' '.join(h_role.tokens)
        print p_str
        print h_str
        parameters = {
            "p": p_str,
            "h": h_str,
        }
        query_string = urlencode(parameters)
        url = self.base_url + query_string
        json_data = urlopen(url)
        results = load(json_data)
        entailment_code = results['entailment_code']
        return entailment_code

if __name__ == '__main__':
    interface = Entailment_API_interface()
    #p = "I devoured a pizza."
    #h = "I ate food."
    #print interface.get_entailment(p, h)