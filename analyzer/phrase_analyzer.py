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
			pos = phrased_words[0][i]['pos']
			iob = phrased_words[1][i]
			self.__pos_iob_count.insert(pos, iob)
			self.__iob_conn.insert(prev_iob, iob)
			self.__add_iob_count(iob)
			prev_iob = iob
			prev_pos = pos
		
		self.__add_iob_count('O')
		self.__iob_conn.insert(prev_iob, 'O')

	def unpack(self, phrased_words, feature='lemma'):
		ret_phrase_list = []
		feature_list = []
		cur_phrase = ''
		prev_iob = ''
		for i in range(len(phrased_words[0])):
			word = phrased_words[i]
			iob_phrase = word[0].split('-')
			f = word[1][feature]
			if iob_phrase[0] == 'O':
				if prev_iob == 'B' or prev_iob == 'I':
					if len(feature_list) > 0 and cur_phrase != '':
						ret_phrase_list.append((cur_phrase, feature_list))
						feature_list = []
						cur_phrase = ''
			elif iob_phrase[0] == 'B':
				if prev_iob == 'B' or prev_iob == 'I':
					if len(feature_list) > 0 and cur_phrase != '':
						ret_phrase_list.append((cur_phase, feature_list))
						feature_list = [f]
						cur_phrase = iob_phrase[1]
			elif iob_phrase[0] == 'I':
					if prev_iob == 'B' or prev_iob == 'I':
						feature_list.append(f)
						prev_iob = iob_phrase[0]

		if prev_iob == 'B' or prev_iob == 'I':
			if len(feature_list) > 0 and cur_phrase != '':
				ret_phrase_list.append((cur_phase, feature_list))
	
		return ret_phrase_list

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
