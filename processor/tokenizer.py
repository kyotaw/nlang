# -*- coding: utf-8 -*-

import sys
import os 
import pickle
from nlang.base.data.conn_table import ConnectivityTable
from nlang.base.data.vocabulary import WordVocabulary
from nlang.processor.sentencer import Sentencer
from nlang.analyzer.cost_minimization_method import CostMinimizationMethod
from nlang.base.util.util import pp
from nlang.base.system import env
from nlang.base.util.singleton import Singleton

def Tokenizer(plain=False):
    def create_new_instance(cls):
        pickls = env.ready_made_tokenizer()
        if os.path.exists(pickls):
            with open(pickls, 'rb') as f:
                return pickle.load(f)
        return super(Singleton, cls).__new__(cls)
    return TokenizerImpl(new_instance_func=None if plain else create_new_instance)

class TokenizerImpl(Singleton):
    def __init__(self, new_instance_func):
        if not self._Singleton__initialized:
            self.__conn_table = ConnectivityTable(env.connfile_path())
            self.__vocab = WordVocabulary(env.vocabfile_path())
            self.__sentencer = Sentencer()
            self.__analyzer = CostMinimizationMethod(self.__vocab, self.__conn_table)
            
            self._Singleton__initialized = True

    def tag(self, stream):
        words = []
        for sent in self.__sentencer.sentences(stream):
            words += self.__tag(sent)
        return words

    def __tag(self, stream):
        node_list = self.__analyzer.extract_paths(stream)
        eos_node = self.__analyzer.shortest_path_vitervi(node_list, len(stream))
        if not eos_node:
            return []
        return self.__summarize(eos_node)
        
    def __summarize(self, eos_node):
        result = []
        node = eos_node
        while node['prev']:
            result.insert(0, node['data'].get_value())
            node = node['prev']
        return result
