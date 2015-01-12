# -*- coding: utf-8 -*-

import sys
from nlang.base.data.phrase import Phrase
from nlang.base.data.conn_table import ConnectivityTable
from nlang.base.system import env

class Chunker(object):
	def __init__(self):
		self.__phrase = Phrase(env.phrasefile_path())
		self.__iob_conn = ConnectivityTable(env.phrase_iob_connfile_path())
		self.__bos_phrase = self.__phrase.phrase(pos='BOS', phrase='O')
		self.__eos_phrase = self.__phrase.phrase(pos='EOS', phrase='O')

	def phrase(self, tagged_words):
		pos_list = []
		for word in tagged_words:
			pos_list.append(word['pos'])
	
		node_list = self.__extract_phrase_paths(pos_list)
		eos_node = self.__shortest_path_vitervi(node_list, len(pos_list))
		
		return self.__summarize(eos_node, tagged_words)

	def train(self, tagged_words, answer_phrased_words):

		result_words = self.phrase(tagged_words)	
	
		answer_phrase_list = [(word[0], worda[1]['pos']) for word in answer_phrased_words]
		result_phrase_list = [(word[0], worda[1]['pos']) for word in result_words]

		for i in range(result_phrase_list):
			result = result_phrase_list[i]
			answer = answer_phrase_list[i]
			if result != answer:
				right = self.__phrase.phrase(answer[1], answer[0])
				right[2] += 1
				wrong = self.__phrase.phrase(reslut[1], result[0])
				wrong[2] -= 1
			else:
				right = self.__phrase.phrase(answer[1], answer[0])
				right[2] += 1
	
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
				phrases = self.__phrase.extract_phrases(pos_list[i])
				if len(phrases) == 0:
					phrases = [(pos_list[i], 'O', 10)]
			else:
				phrases = [self.__eos_phrase]
		
			start_node_list[i] = []
			for phrase in phrases:
				new_node = {'phrase':phrase, 'total_cost':0, 'prev':None}
				start_node_list[i].append(new_node)
				for left_node in end_node_list[i]:
					left_iob = left_node['phrase'][1]
					right_iob = phrase[1]
					if self.__iob_conn.is_connectable(left_iob, right_iob):
						index = i + 1
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
					left_iob = left_node['phrase'][1]
					right_iob = right_node['phrase'][1]
					total_cost = left_node['total_cost'] + right_node['phrase'][2] + self.__iob_conn.cost(left_iob, right_iob)
						
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

	def __summarize(self, eos_node, tagged_words):
		result = []
		node = eos_node
		while node['prev']:
			if node['phrase'][0] != 'EOS':
				start = node['start_index']
				end = node['end_index']
				word_list = [tagged_words[i]['lemma'] for i in range(start, end)]
				result.insert(0, (node['phrase'][1], word_list))
			node = node['prev']
		return result
