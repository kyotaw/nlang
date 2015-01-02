# -*- coding: utf-8 -*-

from nlang.base.data.trie import Trie

class Phrase(object):

	def __init__(self, file_path):
		self.__phrases = Trie()
		
		self.__phrases.insert(['BOS'], (['BOS'], 'BOS', 0))
		self.__phrases.insert(['EOS'], (['EOS'], 'EOS', 0))

		with open(file_path, 'r') as f:
			line = f.readline()
			while line:
				tokens = line[:-1].split('\t')
				if len(tokens) < 3:
					continue
				
				pos_list = tokens[0].split(' ')
				self.__phrases.insert(pos_list, (pos_list, tokens[1], int(tokens[2])))
				line = f.readline()

	def phrase(self, pos_list, phrase):
		not_found = ([], '', 0)
		cands = self.__phrases.common_prefix_search(pos_list)
		for p in cands:
			if phrase == p[1]:
				return p
		return not_found

	def extract_phrases(self, pos_list):
		return self.__phrases.common_prefix_search(pos_list)	


