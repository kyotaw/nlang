# -*- coding: utf-8 -*-

#from nlang.base.data.trie import Trie
from nlang.base.data.trie import ArrayTrie
from nlang.base.data.vocab_word import VocabWord
from nlang.base.data.tagged_word import TaggedWord
from nlang.base.util.util import *


class Word(object):
    def __init__(self, raw_word):
        self._raw = raw_word

    def get_value(self):
        return self._raw

    def get_hook(self):
        return self._raw.tag

    def get_length(self):
        return self._raw.length

    def is_bos(self):
        return True if self._raw.tag == 'BOS' else False

    def is_eos(self):
        return True if self._raw.tag == 'EOS' else False

    def _get_cost(self):
        return self._raw.cost

    def _set_cost(self, value):
        self._raw.cost = value

    cost = property(_get_cost, _set_cost)


class WordVocabulary(object):
    def __init__(self, file_path):
        self._words = Trie()

        self._words.insert('BOS', TaggedWord({'lemma': 'BOS', 'pron': 'BOS', 'pos': ['BOS'], 'cost': 0, 'length': 1}))
        self._words.insert('EOS', TaggedWord({'lemma': 'EOS', 'pron': 'EOS', 'pos': ['EOS'], 'cost': 0, 'length': 1}))

        with open(file_path, 'r') as f:
            line = f.readline()
            while line:
                word = TaggedWord(VocabWord(line))
                self._words.insert(word.lemma, word)
                line = f.readline()

    def extract_vocabulary(self, stream):
        words = self._words.common_prefix_search(stream)
        if len(words) == 0:
            words = self._assume_unknown_word(stream)
        return [Word(w) for w in words]

    def get_bos(self):
        return self._get_word('BOS', 'BOS')

    def get_eos(self):
        return self._get_word('EOS', 'EOS')

    def _get_word(self, lemma, pos):
        not_found = Word(TaggedWord())
        cands = self._words.common_prefix_search(lemma)
        for w in cands:
            if w.lemma == lemma and w.tag == pos:
                return Word(w)
        return not_found

    def _assume_unknown_word(self, stream):
        length = len(stream)
        if length == 0:
            return []
        prev_type = ''
        last_index = 0
        for i in range(length):
            char_type = get_char_type(stream[i])
            if prev_type != '' and prev_type != char_type:
                break
            prev_type = char_type
            last_index = i

        unk_word = stream[:last_index + 1]
        return [TaggedWord({'lemma': unk_word, 'pron': 'UNK', 'base': 'UNK', 'pos': ['UNK'], 'cost': 10, 'length': len(unk_word)})]
