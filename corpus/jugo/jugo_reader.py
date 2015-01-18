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
	    return [TaggedWord(
	        lemma=w.lemma('nlang'),
		pron=w.pron('nlang'),
		pos=w.pos('nlang'),
		conj_form=w.conj_form('nlang'),
		conj_type=w.conj_type('nlang'),
		base=w.base('nlang')) for w in self.vocabulary]

        def phrased_words(self):
	    words = []
	    for v in self.vocabulary:
	        words.append(
		    (v.phrase(),
		    TaggedWord(
			lemma=v.lemma('nlang'),
			pron=v.pron('nlang'),
			pos=v.pos('nlang'),
			conj_form=v.conj_form('nlang'),
			conj_type=v.conj_type('nlang'),
			base=v.base('nlang')),
		    ))
	    return words
            
