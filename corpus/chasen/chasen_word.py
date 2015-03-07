# -*- coding: utf-8 -*-

from nlang.corpus.chasen.chasen_type import ChasenTagTable
from nlang.corpus.chasen.chasen_type import ChasenInvertTable


class ChasenWord(object):
    def __init__(self, raw_str):
        self.lemma = ''
        self.pron = ''
        self.base = ''
        self.pos = []
        self.conj_type = ''
        self.conj_form = ''
        self.is_bos = False
        self.is_eos = False

        tokens = raw_str.split('\t')
        self._extract(tokens)

    def _extract(self, tokens):
        if len(tokens) not in [1, 4, 6]:
            raise Exception('invalid corpus line : ' + '\t'.join(tokens))

        if tokens[0] == 'BOS':
            self.is_bos = True
            self.lemma = self.pron = self.base = 'BOS'
            return
        if tokens[0] == 'EOS':
            self.is_eos = True
            self.lemma = self.pron = self.base = 'EOS'
            return

        self.lemma = tokens[0]
        self.pron = tokens[1]
        self.base = tokens[2]
        parts = tokens[3].split('-')
        for p in parts:
            self.pos.append(p)
        if len(tokens) == 6:
            self.conj_type = tokens[4]
            self.conj_form = tokens[5]
        else:
            self.conj_type = ''
            self.conj_form = ''
    
    def __eq__(self, other):
        return ((self.lemma, self.pron, self.base, self.pos, self.conj_type, self.conj_form) ==
                (other.lemma, other.pron, other.base, other.pos, other.conj_type, other.conj_form))

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        return self.lemma < other.lemma

    def __le__(self, other):
        return self.lemma <= other.lemma

    def __gt__(self, other):
        return self.lemma > other.lemma

    def __ge__(self, other):
        return self.lemma >= other.lemma
