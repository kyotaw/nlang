# -*- coding: utf-8 -*-

from nlang.base.data.trie import Trie

class Clause(object):

	def __init__(self, file_path):
		self.__clauses = Trie()
		
		self.__clauses.insert('BOS', ['BOS', 'O', 0])
		self.__clauses.insert('EOS', ['EOS', 'O', 0])

		with open(file_path, 'r') as f:
			line = f.readline()
			while line:
				tokens = line[:-1].split('\t')
				if len(tokens) < 3:
					continue
				
				pos = tokens[0]
				self.__clauses.insert(pos, [pos, tokens[1], int(tokens[2])])
				line = f.readline()

	def clause(self, pos, clause):
		not_found = ['', '', 0]
		cands = self.__clauses.get(pos)
		for p in cands:
			if clause == p[1]:
				return p
		return not_found

	def extract_clauses(self, pos):
		return self.__clauses.get(pos)

	def dump(self):
            return self.__clauses.dump()


