# -*- coding: utf-8 -*-

import sys
from nlang.base.data.phrase import Phrase
from nlang.base.data.conn_table import ConnectivityTable
from nlang.base.system import env

class Chunker(object):
	def __init__(self):
		self.__phrases = Phrase(env.phrasefile_path())
		self.__iob_conn = ConnectivityTable(env.phrase_iob_connfile_path())
		self.__bos_phrase = self.__phrases.phrase(pos='BOS', phrase='O')
		self.__eos_phrase = self.__phrases.phrase(pos='EOS', phrase='O')
		self.__penalty = 1

	def phrase(self, tagged_words):
		return self.__phrase(tagged_words, self.__get_phrase_cost_func(), self.__get_conn_cost_func())

	def train(self, tagged_words, answer_phrased_words):
		answer_phrase_list = [(word[0], word[1]['pos']) for word in answer_phrased_words]

		result_words = self.__phrase(tagged_words, self.__get_phrase_cost_func(answer_phrase_list), self.__get_conn_cost_func(answer_phrase_list))
		
		result_phrase_list = [(word[0], word[1]['pos']) for word in result_words]
		
		if result_phrase_list != answer_phrase_list:
			for i in range(len(result_phrase_list)):
				answer = answer_phrase_list[i]
				result = result_phrase_list[i]
				if result != answer:
					right = self.__phrases.phrase(answer[1], answer[0])
					right[2] -= 1
					wrong = self.__phrases.phrase(result[1], result[0])
					wrong[2] += 1
					if i != 0:
						right_cost = self.__iob_conn.cost(answer_phrase_list[i-1][0], answer[0])
						self.__iob_conn.set_cost(answer_phrase_list[i-1][0], answer[0], right_cost - 1)
						wrong_cost = self.__iob_conn.cost(result_phrase_list[i-1][0], result[0])
						self.__iob_conn.set_cost(result_phrase_list[i-1][0], result[0], wrong_cost + 1)
			return False
		
		return True

	def __phrase(self, tagged_words, phrase_cost_func, conn_cost_func):
		pos_list = []
		for word in tagged_words:
			pos_list.append(word['pos'])
	
		node_list = self.__extract_phrase_paths(pos_list)
		eos_node = self.__shortest_path_vitervi(node_list, len(pos_list), phrase_cost_func, conn_cost_func)
		
		return self.__summarize(eos_node, tagged_words)

	def __extract_phrase_paths(self, pos_list):
		bos_node = {'phrase':self.__bos_phrase, 'total_cost':0, 'prev':None, 'start_index':-1}
		start_node_list = {}
		end_node_list = {}
		end_node_list[0] = [bos_node]

		length = len(pos_list)
		for i in range(0, length + 1):
			if i not in end_node_list:
				continue

			if i < length:
				phrases = self.__phrases.extract_phrases(pos_list[i])
				if len(phrases) == 0:
					phrases = [(pos_list[i], 'O', 10)]
			else:
				phrases = [self.__eos_phrase]
		
			start_node_list[i] = []
			for phrase in phrases:
				new_node = {'phrase':phrase, 'total_cost':0, 'prev':None, 'start_index':i}
				start_node_list[i].append(new_node)
				for left_node in end_node_list[i]:
					left_iob = left_node['phrase'][1]
					right_iob = phrase[1]
					if self.__iob_conn.is_connectable(left_iob, right_iob):
						index = i + 1
						if index not in end_node_list:
							end_node_list[index] = []
						if new_node not in end_node_list[index]:
							end_node_list[index].append(new_node)
	
		return (start_node_list, end_node_list)

	def __shortest_path_vitervi(self, node_list, length, phrase_cost_func, conn_cost_func):
		for i in range(length+1):
			start_nodes = node_list[0][i] if i in node_list[0] else []
			for right_node in start_nodes:
				end_nodes = node_list[1][i] if i in node_list[1] else []
				min_cost = sys.maxint
				min_cost_nodes = []
				for left_node in end_nodes:
					left_iob = left_node['phrase'][1]
					right_iob = right_node['phrase'][1]
					total_cost = left_node['total_cost'] + phrase_cost_func(right_node) + conn_cost_func(left_node, right_node)
						
					if total_cost < min_cost:
						min_cost = total_cost
						min_cost_nodes = [left_node]
					elif total_cost == min_cost:
						min_cost = total_cost
						min_cost_nodes.append(left_node)
			
				if len(min_cost_nodes) > 0:
					right_node['total_cost'] = min_cost
					right_node['prev'] = min_cost_nodes[0]
		
		return node_list[1][length+1][0]
	
	def __get_phrase_cost_func(self, answer_phrase_list=None):
		if answer_phrase_list:
			def get_phrase_cost_with_penalty(node):
				pos = node['phrase'][0]
				cost = node['phrase'][2]
				if pos == 'BOS' or pos == 'EOS':
					return cost
				answer_iob = answer_phrase_list[node['start_index']][0]
				node_iob = node['phrase'][1]
				return cost + self.__penalty if answer_iob == node_iob else cost
			return get_phrase_cost_with_penalty
		else:
			def get_phrase_cost(node):
				return node['phrase'][2]
			return get_phrase_cost
	
	def __get_conn_cost_func(self, answer_phrase_list=None):
		if answer_phrase_list:
			def get_conn_cost_with_penalty(left_node, right_node):
				left_pos = left_node['phrase'][0]
				right_pos = right_node['phrase'][0]
				left_iob = left_node['phrase'][1]
				right_iob = right_node['phrase'][1]
				cost = self.__iob_conn.cost(left_iob, right_iob)
				if left_pos == 'BOS' or left_pos == 'EOS' or right_pos == 'BOS' or right_pos == 'EOS':
					return cost

				left_answer_iob = answer_phrase_list[left_node['start_index']][0]
				right_answer_iob = answer_phrase_list[right_node['start_index']][0]
				return cost + self.__penalty if left_answer_iob == left_iob and right_answer_iob == right_iob else cost
			return get_conn_cost_with_penalty
		else:
			def get_conn_cost(left_node, right_node):
				left_iob = left_node['phrase'][1]
				right_iob = right_node['phrase'][1]
				return self.__iob_conn.cost(left_iob, right_iob)
			return get_conn_cost
				
				
	def __summarize(self, eos_node, tagged_words):
		result = []
		node = eos_node
		while node['prev']:
			if node['phrase'][0] != 'EOS':
				start = node['start_index']
				result.insert(0, (node['phrase'][1], tagged_words[start]))
			node = node['prev']
		return result
	
	def __unpack(self, phrased_words, feature):
		ret_phrase_list = []
		feature_list = []
		cur_phrase = ''
		prev_iob = ''
		for i in range(len(phrased_words[0])):
			word = phrased_words[i]
			iob_phrase = word[0].split('-')
			f = word[1][feature] if feature else word[1]
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
	
