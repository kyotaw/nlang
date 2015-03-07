# -*- coding: utf-8 -*-

import sys
import os
import pickle

import bz2

from nlang.base.data.conn_table import ConnectivityTable
from nlang.base.data.vocabulary import WordVocabulary, UnicodeRangeWordVocabulary
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
                return pickle.loads(bz2.decompress(f.read()))
        return super(Singleton, cls).__new__(cls)
    return TokenizerImpl(new_instance_func=None if plain else create_new_instance)


class TokenizerImpl(Singleton):
    def __init__(self, new_instance_func):
        if not self._initialized:
            self._conn_table = ConnectivityTable(env.connfile_path())
            self._vocab = WordVocabulary(env.vocabfile_path())
            # self._vocab = UnicodeRangeWordVocabulary()
            self._sentencer = Sentencer()
            self._analyzer = CostMinimizationMethod(self._vocab, self._conn_table)

            self._initialized = True

    def tag(self, stream):
        words = []
        for sent in self._sentencer.sentences(stream):
            words += self._tag(sent)
        return words

    def _tag(self, stream):
        node_list = self._analyzer.extract_paths(stream)
        eos_node = self._analyzer.shortest_path_vitervi(node_list, len(stream))
        if not eos_node:
            return []
        return self._summarize(eos_node)

    def _summarize(self, eos_node):
        result = []
        node = eos_node['prev']
        while node['prev']:
            result.insert(0, node['data'].get_value())
            node = node['prev']
        return result
