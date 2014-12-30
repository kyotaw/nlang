# -*- coding: utf-8 -*-

from nlang.base.data.tagged_word import TaggedWord
from nlang.corpus.chasen.chasen_word import ChasenWord

class ChasenCorpusWriter(object):

	def __init__(self, file_path, tagged_words):
		with open(file_path, 'w') as f:
			for word in tagged_words:
				if word['lemma'] == 'BOS' or word['lemma'] == 'EOS':
					continue
				chasen = ChasenWord(word)
				line = chasen.lemma() + '\t'
				line += chasen.pron() + '\t'
				line += chasen.base() + '\t'
				line += '-'.join(chasen.pos())
				if chasen.conj_form():
					line += '\t' + chasen.conj_form() 
				if chasen.conj_type():
					line += '\t' + chasen.conj_type()
				line += u'\n'
				f.write(line.encode('utf-8'))
