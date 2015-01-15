# -*- coding: utf-8 -*-

from nlang.base.data.trie import Trie

class PhraseAnalyzer(object):
	def __init__(self):
		self.__pos_iob_count = Trie()
		self.__iob_count = {}
		self.__iob_conn = Trie()
	
	def analyze(self, phrased_words):
		prev_iob = 'O'
		self.__add_iob_count(prev_iob)
		for i in range(len(phrased_words[0])):
			iob = phrased_words[i][0]
			pos = phrased_words[i][1]['pos']
			self.__pos_iob_count.insert(pos, iob)
			self.__iob_conn.insert(prev_iob, iob)
			self.__add_iob_count(iob)
			prev_iob = iob
			prev_pos = pos
		
		self.__add_iob_count('O')
		self.__iob_conn.insert(prev_iob, 'O')

	def calc_phrase_probability(self):
		phrase_list = []
		for pos_iob in self.__pos_iob_count.dump():
			pos = pos_iob[0]
			iob = pos_iob[1]
			phrase_list.append((
				''.join(pos),
				iob,
				self.__pos_iob_count.count(pos, iob) * 1.0 / self.__iob_count[iob]))
		return phrase_list

	def calc_enter_conn_probability(self):
		conn_list = {}
		for conn in self.__iob_conn.dump():
			left_iob = ''.join(conn[0])
			right_iob = conn[1]
			if left_iob not in conn_list:
				conn_list[left_iob] = []
			conn_list[left_iob].append((right_iob, self.__iob_conn.count(left_iob, right_iob) * 1.0 / self.__iob_count[left_iob]))
		return conn_list

	def __add_iob_count(self, iob):
		if iob in self.__iob_count:
			self.__iob_count[iob] += 1
		else:
			self.__iob_count[iob] = 1
