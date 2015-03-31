# -*- coding: utf-8 -*-

import os
import pickle

import bz2

from nlang.base.system import env
from nlang.classifier.naive_bayes_classifier import NaiveBayesClassifier
from nlang.base.util.singleton import Singleton


def Sentencer(plain=True):
    def create_new_instance(cls):
        pickls = env.ready_made_sentencer()
        if os.path.exists(pickls):
            with open(pickls, 'rb') as f:
                return pickle.loads(bz2.decompress(f.read()))
        return super(Singleton, cls).__new__(cls)
    return SentencerImpl(None if plain else create_new_instance)


class SentencerImpl(Singleton):
    @staticmethod
    def get_feature(c, prev_char, next_char):
        return {'punct': c, 'prev_char': prev_char, 'next_char': next_char}

    def __init__(self, new_instance_func):
        if not self._initialized:
            self._classifier = NaiveBayesClassifier()
            self._initialized = True

    def sentences(self, text):
        sent = ''
        prev_char = ''
        for i in range(len(text)):
            c = text[i]
            next_char = text[i + 1] if i + 1 < len(text) else ''
            if c == '\n':
                continue
            if self._classifier.classify(SentencerImpl.get_feature(c, prev_char, next_char)) == 'True':
                yield sent + c
                sent = ''
            else:
                sent += c
            prev_char = c
        if len(sent) > 0:
            yield sent
        raise StopIteration

    def train(self, data):
        self._classifier.train(data)
