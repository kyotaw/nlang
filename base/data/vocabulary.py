# -*- coding: utf-8 -*-

from nlang.base.data.trie import Trie
from nlang.base.data.tagged_word import TaggedWord

class Vocabulary:
	def __init__(self, file_path):
		self.__words = Trie()
		
		self.__words.insert('BOS', TaggedWord(lemma='BOS', pron='BOS', pos='BOS', cost=0, length=1))
		self.__words.insert('EOS', TaggedWord(lemma='EOS', pron='EOS', pos='EOS', cost=0, length=1))

		with open(file_path, 'r') as f:
			line = f.readline()
			while line:
				tokens = line[:-1].split('\t')
				if len(tokens) < 5:
					continue
				
			#	conj_form = ''
			#	conj_type = ''
			#	if len(tokens) == 4:
			#		cost = tokens[3]
			#	elif len(tokens) >= 5:
			#		conj_form = tokens[3]
			#		conj_type = tokens[4]
			#		cost = tokens[5]
					
				word = TaggedWord(
					lemma=tokens[0].decode('utf-8'),
					pron=tokens[1].decode('utf-8'),
					base=tokens[2].decode('utf-8'),
					pos=tokens[3],
					cost=tokens[4],
					length=len(tokens[0].decode('utf-8'))
				)
				self.__words.insert(word['lemma'], word)
				line = f.readline()

	def word(self, lemma, pos):
		not_found = TaggedWord()
		cands = self.__words.common_prefix_search(lemma)
		for w in cands:
			if w['lemma'] == lemma and w['pos'] == pos:
				return w	
		return not_found
			
	def extract_words(self, stream):
		return self.__words.common_prefix_search(stream)

	
