# -*- coding: utf-8 -*-

from nlang.corpus.analyzer.connectivity_analyzer import ConnectivityAnalyzer
from nlang.corpus.reader.chasen import *
from nlang.base.util.util import pp
import pprint

all_path = True

analyzer = ConnectivityAnalyzer()
reader = ChasenCorpusReader('../../testdata/0001.chasen', '', 'utf-8')
analyzer.analyze(reader.tagged_words())

left_pos = 'N-PRON-GEN'
right_pos = 'J-JB'
prob = analyzer.probability(left_pos, right_pos)
print pp(u'prob of ' + left_pos + ' to ' + right_pos + ' : ' + str(prob))
