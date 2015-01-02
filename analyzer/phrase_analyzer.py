# -*- coding: utf-8 -*-

from nlang.base.data.trie import Trie

class PhraseAnalyzer(object):
	def __init__(self):
		self.__phrase_pattern = Trie()
		self.__phrase_count = {}
		self.__pos_count = {}
		self.__enter_conn = Trie()
		self.__exit_conn = Trie()

	def analyze(self, phrased_words):
		pos_list = []
		cur_phrase = ''
		prev_iob = ''
		prev_pos = 'BOS'
		self.__add_pos_count(prev_pos)
		for i in range(len(phrased_words[0])):
			pos = phrased_words[0][i]['pos']
			iob_phrase = phrased_words[1][i].split('-')
			if iob_phrase[0] == 'O':
				if prev_iob == 'B' or prev_iob == 'I':
					if len(pos_list) > 0 and cur_phrase != '':
						self.__phrase_pattern.insert(pos_list, cur_phrase)
						self.__exit_conn.insert(prev_pos, pos)
						self.__add_phrase_count(cur_phrase)
				pos_list = []
				cur_phrase = ''
			elif iob_phrase[0] == 'B':
				if prev_iob == 'B' or prev_iob == 'I':
					if len(pos_list) > 0 and cur_phrase != '':
						self.__phrase_pattern.insert(pos_list, cur_phrase)
						self.__exit_conn.insert(prev_pos, pos)
						self.__add_phrase_count(cur_phrase)
				pos_list = [pos]
				self.__enter_conn.insert(prev_pos, pos)
				cur_phrase = iob_phrase[1]
			elif iob_phrase[0] == 'I':
				if prev_iob == 'B' or prev_iob == 'I':
					pos_list.append(pos)
			
			self.__add_pos_count(pos)
			prev_iob = iob_phrase[0]
			prev_pos = pos

		if prev_iob == 'B' or prev_iob == 'I':
			if len(pos_list) > 0 and cur_phrase != '':
				self.__phrase_pattern.insert(pos_list, cur_phrase)
				self.__exit_conn.insert(prev_pos, 'EOS')
				self.__add_phrase_count(cur_phrase)
	
		self.__add_pos_count('EOS')

	def calc_phrase_probability(self):
		phrase_list = []
		for pattern_phrase in self.__phrase_pattern.dump():
			pattern = pattern_phrase[0]
			phrase = pattern_phrase[1]
			phrase_list.append((
				' '.join(pattern),
				phrase,
				self.__phrase_pattern.count(pattern, phrase) * 1.0 / self.__phrase_count[phrase]))
		return phrase_list

	def calc_enter_conn_probability(self):
		conn_list = {}
		for conn in self.__enter_conn.dump():
			left_pos = ''.join(conn[0])
			right_pos = conn[1]
			if left_pos not in conn_list:
				conn_list[left_pos] = []
			conn_list[left_pos].append((right_pos, self.__enter_conn.count(left_pos, right_pos) * 1.0 / self.__pos_count[left_pos]))
		return conn_list

	def calc_exit_conn_probability(self):
		conn_list = {}
		for conn in self.__exit_conn.dump():
			left_pos = ''.join(conn[0])
			right_pos = conn[1]
			if left_pos not in conn_list:
				conn_list[left_pos] = []
			conn_list[left_pos].append((right_pos, self.__exit_conn.count(left_pos, right_pos) * 1.0 / self.__pos_count[left_pos]))
		return conn_list

	def __add_phrase_count(self, phrase):
		if phrase in self.__phrase_count:
			self.__phrase_count[phrase] += 1
		else:
			self.__phrase_count[phrase] = 1

	def __add_pos_count(self, pos):
		if pos in self.__pos_count:
			self.__pos_count[pos] += 1
		else:
			self.__pos_count[pos] = 1
