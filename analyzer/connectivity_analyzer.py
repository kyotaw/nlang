# -*- coding: utf-8 -*-

from nlang.base.data.trie import Trie
from nlang.base.data.tagged_word import TaggedWord

class ConnectivityAnalyzer:
	def __init__(self):
		self.connect_table = {}
		self.pos_count = {}
		self.bigram_count = Trie()

	def probability(self, left_pos, right_pos):
		if left_pos not in self.pos_count:
			return 0
		return self.bigram_count.count(left_pos, right_pos) * 1.0 / self.pos_count[left_pos]

	def analyze(self, tagged_words):
		cur_left = u'BOS'
		for right_word in tagged_words:
			right_pos = right_word['pos']
			self.__add_connectable_pos(cur_left, right_pos)
			self.bigram_count.insert(cur_left, right_pos)
			self.__add_pos_count(cur_left)
			cur_left = right_pos

		self.__add_connectable_pos(cur_left, 'EOS')
		self.bigram_count.insert(cur_left, 'EOS')
		self.__add_pos_count(cur_left)
		
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

