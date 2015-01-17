# -*- coding: utf-8 -*-

from nlang.corpus.analyzer.vocabulary_analyzer import VocabularyAnalyzer
from nlang.corpus.reader.chasen import *
from nlang.base.util.util import pp
import pprint

all_path = True

analyzer = VocabularyAnalyzer()
reader = ChasenCorpusReader('../../testdata/0001.chasen', '', 'utf-8')
analyzer.analyze(reader.tagged_words())

prob = analyzer.probability(u'私', 'N-PRON-GEN')
print pp(u'prob of 私: ' + str(prob))

