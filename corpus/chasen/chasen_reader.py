# -*- coding: utf-8 -*-

import glob
import codecs
import os
from nlang.base.data.tagged_word import TaggedWord
from nlang.corpus.chasen.chasen_word import ChasenWord

class ChasenCorpusReader(object):
	def __init__(self, path, file_pattern, encoding):
		if file_pattern == '':
			self.file_list = glob.glob(os.path.expanduser(path))
		else:
			self.file_list = glob.glob(os.path.expanduser(path) + '/' + file_pattern)
		self.encoding = encoding
		self.vocabulary = []
		for file in self.file_list:
			self.__read(file, encoding)

	def words(self):
		return [w.lemma for w in self.vocabulary]

	def tagged_words(self):
		return [TaggedWord(
			lemma=w.lemma('nlang'),
			pron=w.pron('nlang'),
			pos=w.pos('nlang'),
			conj_form=w.conj_form('nlang'),
			conj_type=w.conj_type('nlang'),
			base=w.base('nlang')) for w in self.vocabulary]

	def __read(self, file_path, encoding):
		f = codecs.open(file_path, 'r', encoding)
		for line in f.readlines():
			w = ChasenWord(line)
			if (w.valid):
				self.vocabulary.append(w)
