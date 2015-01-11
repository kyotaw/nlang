# -*- coding: utf-8 -*-

from nlang.base.data.trie import Trie

class Phrase(object):

	def __init__(self, file_path):
		self.__phrases = Trie()
		
		self.__phrases.insert('BOS', ['BOS', 'O', 0])
		self.__phrases.insert('EOS', ['EOS', 'O', 0])

		with open(file_path, 'r') as f:
			line = f.readline()
			while line:
				tokens = line[:-1].split('\t')
				if len(tokens) < 3:
					continue
				
				pos = tokens[0]
				self.__phrases.insert(pos, [pos, tokens[1], int(tokens[2])])
				line = f.readline()

	def phrase(self, pos, phrase):
		not_found = ['', '', 0]
		cands = self.__phrases.get(pos)
		for p in cands:
			if phrase == p[1]:
				return p
		return not_found

	def extract_phrases(self, pos):
		return self.__phrases.get(pos)	


