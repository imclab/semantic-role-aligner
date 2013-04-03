# -*- coding: utf-8 -*-
'''
http://localhost:8001/e?p=i%20ate%20pizza&h=i%20ate%20food
'''
from json import load
from urllib import urlopen
from urllib import urlencode


class Entailment_API_interface(object):

    def __init__(self):
        #self.base_url = 'http://localhost:8001/e?'
        self.base_url = 'http://localhost:8001/entail?'

    def get_sub_entailment(self, p_role, h_role):
        h_str = ' '.join(h_role.tokens)
        p_str = ' '.join(p_role.tokens)
        print p_str
        print h_str
        parameters = {
            "p": p_str,
            "h": h_str,
            "mark": 'False'
        }
        query_string = urlencode(parameters)
        url = self.base_url + query_string
        return self.query(url)

    def get_ins_entailment(self, h_role):
        h_str = ' '.join(h_role.tokens)
        print h_str
        parameters = {
            "p": 'INS',
            "h": h_str,
            "mark": 'False'
        }
        query_string = urlencode(parameters)
        url = self.base_url + query_string
        return self.query(url)

    def get_del_entailment(self, p_role):
        p_str = ' '.join(p_role.tokens)
        print p_str
        parameters = {
            "p": p_str,
            "h": 'DEL',
            "mark": 'False'
        }
        query_string = urlencode(parameters)
        url = self.base_url + query_string
        return self.query(url)

    def query(self, url):
        print url
        json_data = urlopen(url)
        results = load(json_data)
        return results['entailment_code']


if __name__ == '__main__':
    interface = Entailment_API_interface()