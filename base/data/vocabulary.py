# -*- coding: utf-8 -*-

import threading

from nlang.base.data.trie import Trie
from nlang.base.data.double_array_trie import DoubleArrayTrie
from nlang.base.data.vocab_word import VocabWord
from nlang.base.data.tagged_word import TaggedWord
from nlang.base.util.util import get_char_type
from nlang.base.util.unicode_util import unicode_range, code_point
from nlang.base.system import env


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

    def get_all_words(self):
        return [key_val[1] for key_val in self._words.dump()]

    def _get_word(self, lemma, pos):
        not_found = Word(TaggedWord())
        cands = self._words.get(lemma)
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


class UnicodeRangeWordVocabulary(object):
    @staticmethod
    def _init_vocaburaly(self, file_path, uni_range, lock):
        wv = WordVocabulary(file_path)
        lock.acquire()
        self._ranged_vocabulary_map[uni_range] = wv
        lock.release()

    def __init__(self):
        self._ranged_vocabulary_map = {}
        self._bos = TaggedWord({'lemma': 'BOS', 'pron': 'BOS', 'pos': ['BOS'], 'cost': 0, 'length': 1})
        self._eos = TaggedWord({'lemma': 'EOS', 'pron': 'EOS', 'pos': ['EOS'], 'cost': 0, 'length': 1})

        init_threads = []
        lock = threading.Lock()

        vocab_folder = env.vocabfolder_path()
        for uni_range in unicode_range:
            file_name = '_'.join(map(lambda v: hex(v), uni_range))
            file_path = vocab_folder + file_name
            with open(file_path) as f:
                if not f.readline():
                    continue
            thread = threading.Thread(target=UnicodeRangeWordVocabulary._init_vocaburaly, args=(self, file_path, uni_range, lock))
            thread.start()
            init_threads.append(thread)

        for thread in init_threads:
            thread.join()

    def extract_vocabulary(self, stream):
        if not stream:
            return []

        wv = self._get_word_vocabulary(stream)
        if wv is None:
            return []
        return wv.extract_vocabulary(stream)

    def get_bos(self):
        wv = self._get_word_vocabulary('BOS')
        if wv is None:
            return []
        return wv.get_bos()

    def get_eos(self):
        wv = self._get_word_vocabulary('EOS')
        if wv is None:
            return []
        return wv.get_eos()

    def _get_word_vocabulary(self, stream):
        code = code_point(stream[0])
        for uni_range, wv in self._ranged_vocabulary_map.items():
            if uni_range[0] <= code and code <= uni_range[1]:
                return wv
        return None
