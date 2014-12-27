# -*- coding: utf-8 -*-

from nlang.base.data.trie import Trie

class ConnectivityAnalyzer:
	def __init__(self):
		self.connect_table = {}
		self.pos_count = {}
		self.bigram_count = Trie()

	def analyze(self, tagged_words):
		sentence = []
		for word in tagged_words:
			if word[2] == 'SY-PE' or word[2] == 'EOS':
				self.__analyze(sentence)
				del sentence[:]
			else:
				sentence.append(word[2])

	def probability(self, left_pos, right_pos):
		if left_pos not in self.pos_count:
			return 0
		return self.bigram_count.count(left_pos, right_pos) * 1.0 / self.pos_count[left_pos]

	def __analyze(self, sentence):
		cur_left = u'BOS'
		for right_pos in sentence:
			self.__add_connectable_pos(cur_left, right_pos)
			self.bigram_count.insert(cur_left, right_pos)
			self.__add_pos_count(cur_left)
			cur_left = right_pos

		self.__add_connectable_pos(cur_left, 'EOS')
		self.__add_connectable_pos(cur_left, 'SY-PE')
		self.bigram_count.insert(cur_left, 'EOS')
		self.bigram_count.insert(cur_left, 'SY-PE')
		self.__add_pos_count(cur_left)
		
		self.__add_connectable_pos('SY-PE', 'EOS')
		self.bigram_count.insert('SY-PE', 'EOS')
		self.__add_pos_count('SY-PE')

	def __add_pos_count(self, pos):
		if pos in self.pos_count:
			self.pos_count[pos] += 1
		else:
			self.pos_count[pos] = 1
	
	def __add_connectable_pos(self, left_pos, right_pos):
		if left_pos not in self.connect_table:
			self.connect_table[left_pos] = []
		if right_pos not in self.connect_table[left_pos]:
			self.connect_table[left_pos].append(right_pos)

