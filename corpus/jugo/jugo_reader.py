# -*- coding: utf-8 -*-

import os
from nlang.corpus.jugo.jugo_word import JugoWord
from nlang.base.data.tagged_word import TaggedWord


class JugoCorpusReader:
    def __init__(self, file_path):
        self.words = None
        self._read(os.path.expanduser(file_path))

    def tagged_words(self):
        return [TaggedWord(w) for w in self.words if not w.is_bos and not w.is_eos]

    def claused_words(self):
        return [(w.clause, TaggedWord(w)) for w in self.words if not w.is_bos and not w.is_eos]

    def _read(self, file_path):
        with open(file_path, 'r') as f:
            self.words = [JugoWord(line[:-1]) for line in f.readlines()]
