# -*- coding: utf-8 -*-

import os
from nlang.base.data.tagged_word import TaggedWord
from nlang.corpus.chasen.chasen_word import ChasenWord


class ChasenCorpusReader(object):
    def __init__(self, file_path):
        self.words = None
        self._read(os.path.expanduser(file_path))

    def tagged_words(self):
        return [TaggedWord(w) for w in self.words if not w.is_bos and not w.is_eos]

    def _read(self, file_path):
        with open(file_path, 'r') as f:
            self.words = [ChasenWord(line[:-1]) for line in f.readlines()]
