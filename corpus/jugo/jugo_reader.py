# -*- coding: utf-8 -*-

import codecs
from nlang.corpus.base.base_reader import BaseReader
from nlang.corpus.jugo.jugo_word import JugoWord
from nlang.base.data.tagged_word import TaggedWord

class JugoCorpusReader(BaseReader):
	def __init__(self, path, file_pattern='', encoding='utf-8'):
		super(JugoCorpusReader, self).__init__(path, file_pattern, encoding)
		
	def read(self, file_path, encoding):
		f = codecs.open(file_path, 'r', encoding)
		for line in f.readlines():
			w = JugoWord(line)
			if w.valid:
				self.vocabulary.append(w)
		f.close()

	def tagged_words(self):
		words = []
		phrase = []
		for v in self.vocabulary:
			words.append(
				TaggedWord(
					lemma=v.lemma('nlang'),
					pron=v.pron('nlang'),
					pos=v.pos('nlang'),
					conj_form=v.conj_form('nlang'),
					conj_type=v.conj_type('nlang'),
					base=v.base('nlang')))
			phrase.append(v.phrase())
		return (words, phrase)

