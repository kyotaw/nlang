# -*- coding: utf-8 -*-

import sys
from nlang.base.data.phrase import Phrase
from nlang.base.data.conn_table import ConnectivityTable
from nlang.base.system import env

class Chunker(object):
	def __init__(self):
		self.__phrase = Phrase(env.phrasefile_path())
		self.__enter_conn = ConnectivityTable(env.phrase_enter_connfile_path())
		self.__exit_conn = ConnectivityTable(env.phrase_exit_connfile_path())
		self.__bos_phrase = self.__phrase.phrase(pos_list=['BOS'], phrase='BOS')
		self.__eos_phrase = self.__phrase.phrase(pos_list=['EOS'], phrase='EOS')

	def phrase(self, tagged_words):
		pos_list = []
		for word in tagged_words:
			if word['pos'] != 'BOS' and word['pos'] != 'EOS':
				pos_list.append(word['pos'])
	
		node_list = self.__extract_phrase_paths(pos_list)
		eos_node = self.__shortest_path_vitervi(node_list, len(pos_list))

		result = []
		node = eos_node
		while node['prev']:
			if node['phrase'][1] != 'EOS':
				start = node['start_index']
				end = node['end_index']
				phrase = [node['phrase'][1]]
				for i in range(start, end):
					phrase.append(tagged_words[i+1]['lemma'])
				result.insert(0, phrase)
			node = node['prev']
	
		return result
	
	def __extract_phrase_paths(self, pos_list):
		bos_node = {'phrase':self.__bos_phrase, 'total_cost':0, 'prev':None}
		start_node_list = {}
		end_node_list = {}
		end_node_list[0] = [bos_node]

		length = len(pos_list)
		for i in range(0, length + 1):
			if i not in end_node_list:
				continue

			if i < length:
				phrases = self.__phrase.extract_phrases(pos_list[i:])
				if len(phrases) == 0:
					phrases = [([pos_list[i]], 'O', 10)]
			else:
				phrases = [self.__eos_phrase]
		
			start_node_list[i] = []
			for phrase in phrases:
				new_node = {'phrase':phrase, 'total_cost':0, 'prev':None}
				start_node_list[i].append(new_node)
				for left_node in end_node_list[i]:
					left_pos = left_node['phrase'][0][-1]
					right_pos = phrase[0][0]
					if True or self.__enter_conn.is_connectable(left_pos, right_pos) or left_pos == 'BOS' or right_pos == 'EOS':
						index = i + len(phrase[0])
						new_node['start_index'] = i
						new_node['end_index'] = index
						if index not in end_node_list:
							end_node_list[index] = []
						if new_node not in end_node_list[index]:
							end_node_list[index].append(new_node)
	
		return (start_node_list, end_node_list)

	def __shortest_path_vitervi(self, node_list, length):
		for i in range(length+1):
			start_nodes = node_list[0][i] if i in node_list[0] else []
			for right_node in start_nodes:
				end_nodes = node_list[1][i] if i in node_list[1] else []
				min_cost = sys.maxint
				min_cost_nodes = []
				for left_node in end_nodes:
					left_pos = left_node['phrase'][0][-1]
					right_pos = right_node['phrase'][0][-1]
					total_cost = left_node['total_cost'] + right_node['phrase'][2] + self.__enter_conn.cost(left_pos, right_pos)
						
					if total_cost < min_cost:
						min_cost = total_cost
						min_cost_nodes = [left_node]
					elif total_cost == min_cost:
						min_cost = total_cost
						min_cost_nodes.append(left_node)
			
				if len(min_cost_nodes) > 0:
					right_node['total_cost'] = min_cost
					max_len = -1
					for min_node in min_cost_nodes:
						l = len(min_node['phrase'][0])	+ len(right_node['phrase'][0])
						if max_len < l:
							max_len = l
							right_node['prev'] = left_node
		
		return node_list[1][length+1][0]
