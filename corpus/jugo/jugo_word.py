# -*- coding: utf-8 -*-

from nlang.corpus.chasen.chasen_word import ChasenWord


class JugoWord(ChasenWord):
    def __init__(self, raw_str):
        self.clause = 'O'
        ChasenWord.__init__(self, raw_str)

    def _extract(self, tokens):
        if len(tokens) not in [1, 5, 7]:
            raise Exception('invalid corpus line : ' + '\t'.join(tokens))
        ChasenWord._extract(self, tokens[:-1])

        if len(tokens) == 5:
            self.clause = tokens[4]
        elif len(tokens) == 7:
            self.clause = tokens[6]
