# -*- coding: utf-8 -*-

from nlang.base.util import unicode
from nlang.classifier.naive_bayes_classifier import NaiveBayesClassifier

class Senetencer(object):
    def __init__(self):
        self.__classifier = NaiveBayesClassifier()
        self.__classifier.train([
            ('True', self.__get_feature(u'。')),
            ('True', self.__get_feature(u'.')),
            ('True', self.__get_feature(u'!')),
            ('True', self.__get_feature(u'！')),
            ('True', self.__get_feature(u'?')),
            ('True', self.__get_feature(u'？')),
        ])

    def sentences(self, text):
        sents = []
        sent = u''
        for i in range(len(text)):
            c = text[i]
            if c == '\n':
                continue
            if self.__classifier.classify(self.__get_feature(c)) == 'True':
                sents.append(sent + c)
                sent = u''
            else:
                sent += c
        if len(sent) > 0:
            sents.append(sent)
        return sents

    def __get_feature(self, c):
        return {
            'punct':c,
            'is_ascii':unicode.is_ascii(c),
            'is_alpha_zenkaku':unicode.is_alpha_zenkaku(c),
            'is_hiragana':unicode.is_hiragana(c),
            'is_katakana_zenkaku':unicode.is_katakana_zenkaku(c),
            'is_katakana_hankaku':unicode.is_katakana_hankaku(c),
            'is_kanji':unicode.is_kanji(c)
        }
