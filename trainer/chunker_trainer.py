# -*- coding: utf-8 -*-

from nlang.processor.chunker import Chunker
from nlang.analyzer.phrase_analyzer import PhraseAnalyzer
from nlang.corpus.jugo.jugo_reader import JugoCorpusReader
from nlang.base.util.util import pp

reader = JugoCorpusReader('../testdata/phrase/yahoo-0001.chasen')
jugo_words = reader.tagged_words()

tagged_words = [w[1] for w in jugo_words]

chunker = Chunker()
for i in range(100):
	chunker.train(tagged_words, jugo_words)

rr = chunker.phrase(tagged_words)

result = []
for p in rr:
	result.append((p[0], p[1]['lemma']))

print(pp(result))

