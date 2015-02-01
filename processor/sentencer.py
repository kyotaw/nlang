# -*- coding: utf-8 -*-

import os
import pickle
from nlang.base.util import unicode
from nlang.base.system import env
from nlang.corpus.delim.delim_reader import DelimCorpusReader
from nlang.classifier.naive_bayes_classifier import NaiveBayesClassifier
from nlang.base.util.singleton import Singleton

def Sentencer():
    def create_new_instance(cls):
        pickls = env.ready_made_sentencer()
        if os.path.exists(pickls):
            with open(pickls, 'rb') as f:
                return pickle.load(f)
        return super(Singleton, cls).__new__(cls)
    return SentencerImpl(create_new_instance)

class SentencerImpl(Singleton):
    @staticmethod
    def get_feature(c, prev_char, next_char):
        return {'punct':c, 'prev_char':prev_char, 'next_char':next_char}

    def __init__(self, new_instance_func):
        if not self._Singleton__initialized:
            self.__classifier = NaiveBayesClassifier()
            self._Singleton__initialized = True

    def sentences(self, text):
        sents = []
        sent = u''
        prev_char = u''
        for i in range(len(text)):
            c = text[i]
            next_char = text[i+1] if i+1 < len(text) else u''
            if c == '\n':
                continue
            if self.__classifier.classify(SentencerImpl.get_feature(c, prev_char, next_char)):
                sents.append(sent + c)
                sent = u''
            else:
                sent += c
            prev_char = c
        if len(sent) > 0:
            sents.append(sent)
        return sents

    def train(self, data):
        self.__classifier.train(data)
