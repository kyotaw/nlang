# -*- coding: utf-8 -*-

from nlang.base.data.trie import Trie

class Vocabulary:
	def __init__(self, file_path):
		self.__words = Trie()
		
		self.__words.insert('BOS', {'lemma':'BOS', 'pron':'BOS', 'pos':'BOS', 'cost':0, 'length':1})
		self.__words.insert('EOS', {'lemma':'EOS', 'pron':'EOS', 'pos':'EOS', 'cost':0, 'length':1})

		with open(file_path, 'r') as f:
			line = f.readline()
			while line:
				tokens = line[:-1].split('\t')
				if len(tokens) < 4:
					continue
				word = {
					'lemma':tokens[0].decode('utf-8'),
					'pron':tokens[1].decode('utf-8'),
					'pos':tokens[2],
					'cost':tokens[3],
					'length':len(tokens[0].decode('utf-8'))
				}
				self.__words.insert(word['lemma'], word)
				line = f.readline()

	def word(self, lemma, pos):
		not_found = {'lemmma':'', 'pron':'', 'pos':'', 'cost':0, 'length':0}
		cands = self.__words.common_prefix_search(lemma)
		for w in cands:
			if w['lemma'] == lemma and w['pos'] == pos:
				return w	
		return not_found
			
	def extract_words(self, stream):
		return self.__words.common_prefix_search(stream)

	
