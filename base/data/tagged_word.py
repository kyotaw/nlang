# -*- coding: utf-8 -*-

import sys
from functools import singledispatch

from nlang.corpus.chasen.chasen_word import ChasenWord
from nlang.corpus.jugo.jugo_word import JugoWord
from nlang.base.data.vocab_word import VocabWord
from nlang.corpus.chasen.chasen_type import ChasenTagTable


@singledispatch
def unpack_data(dummy_data, self):
    default = {'lemma': '', 'pron': '', 'base': '', 'pos': [], 'conj_type': '', 'conj_form': '', 'tag': '', 'cost': sys.maxsize, 'length': 0}
    for key, value in default.items():
        if not hasattr(self, key):
            setattr(self, key, value)


@unpack_data.register(dict)
def unpack_dict(data, self):
    unpack_data(None, self)
    for key, value in data.items():
        if hasattr(self, key):
            setattr(self, key, value)
    if 'length' not in data:
        self.length = len(self.lemma)
    if 'tag' not in data:
        self.tag = TaggedWord.tag(self.pos, self.conj_type, self.conj_form)


@unpack_data.register(ChasenWord)
def unpack_chasen(data, self):
    unpack_data(None, self)
    self.lemma = data.lemma
    self.pron = data.pron
    self.base = data.base
    self.pos = list(data.pos)
    self.conj_type = data.conj_type
    self.conj_form = data.conj_form
    self.length = len(data.lemma)
    self.tag = TaggedWord.tag(self.pos, self.conj_type, self.conj_form)


@unpack_data.register(JugoWord)
def unpack_jugo(data, self):
    unpack_chasen(data, self)


@unpack_data.register(VocabWord)
def unpack_vocab(data, self):
    unpack_chasen(data, self)
    self.cost = data.cost


class TaggedWord(object):
    @staticmethod
    def tag(pos, conj_type, conj_form):
        if not pos:
            return ''
        if pos[0] in ['BOS', 'EOS', 'UNK']:
            return pos[0]
        tag = '-'.join(map(lambda p: ChasenTagTable[p], pos))
        if conj_type:
            tag += '-' + ChasenTagTable[conj_type]
        if conj_form:
            tag += '-' + ChasenTagTable[conj_form]
        return tag

    def __init__(self, data=None):
        unpack_data(data, self)

    def __eq__(self, other):
        return ((self.lemma, self.pron, self.base, self.pos, self.conj_type, self.conj_form, self.tag, self.length, self.cost) ==
                (other.lemma, other.pron, other.base, other.pos, other.conj_type, other.conj_form, other.tag, other.length, other.cost))

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
