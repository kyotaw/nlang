# -*- coding: utf-8 -*-

import sys
from nlang.corpus.chasen.chasen_word import ChasenWord


class VocabWord(ChasenWord):
    def __init__(self, raw_str):
        self.cost = sys.maxsize
        ChasenWord.__init__(self, raw_str)

    def _extract(self, tokens):
        if len(tokens) not in [1, 5, 7]:
            raise Exception('invalid corpus line : ' + '\t'.join(tokens))
        ChasenWord._extract(self, tokens[:-1])

        if len(tokens) == 5:
            self.cost = int(tokens[4])
        elif len(tokens) == 7:
            self.cost = int(tokens[6])
