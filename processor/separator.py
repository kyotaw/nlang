# -*- coding: utf-8 -*-

from nlang.base.data.conn_table import ConnectivityTable
from nlang.base.data.vocabulary import Vocabulary
from nlang.base.util.util import pp
from nlang.base.system import env
import sys

class Separator(object):
	def __init__(self):
		self.__conn_table = ConnectivityTable(env.connfile_path())
		self.__vocab = Vocabulary(env.vocabfile_path())
	
	def separate(self, sentence):
		return self.__parse(sentence, tagged=False)	

	def tagg(self, sentence):
		return self.__parse(sentence, tagged=True)

	def __parse(self, sentence, tagged):
		
		bos_entry = self.__vocab.word(lemma='BOS', pos='BOS')
		eos_entry = self.__vocab.word(lemma='EOS', pos='EOS')
		bos_node = {'entry':bos_entry, 'total_cost':0, 'result_id':0}
		node_list = {}
		node_list[0] = [bos_node]
	
		result_candidates = {} 
		result_candidates[bos_node['result_id']] = [bos_entry]

		length = len(sentence)
		for i in range(0, length + 1):
			if i not in node_list:
				continue

			if i < length:
				entries = self.__vocab.extract_words(sentence[i:])
			else:
				entries = [eos_entry]
			
			connected = False
			for entry in entries:
				new_node = {'entry':entry, 'total_cost':0, 'result_id': -1}
				min_cost = sys.maxint
				min_cost_nodes = []
				for left_node in node_list[i]:
					if self.__conn_table.is_connectable(left_node['entry']['pos'], new_node['entry']['pos']):
						total_cost = left_node['total_cost'] + self.__conn_table.cost(left_node['entry']['pos'], new_node['entry']['pos'])
						
						if total_cost < min_cost:
							min_cost = total_cost
							min_cost_nodes = [left_node]
						elif total_cost == min_cost:
							min_cost = total_cost
							min_cost_nodes.append(left_node)
			
				if len(min_cost_nodes) > 0:
					for left_node in min_cost_nodes:
						new_node['total_cost'] = min_cost
						partial_result = result_candidates[left_node['result_id']]
						id = len(result_candidates) + 1
						result_candidates[id] = partial_result + [new_node['entry']]
						new_node['result_id'] = id

					index = i + entry['length']
					if index not in node_list:
						node_list[index] = []
					if new_node not in node_list[index]:
						node_list[index].append(new_node)
		
		min_id = sys.maxint
		for	k, v in result_candidates.items():
			if k < min_id and v[-1]['lemma'] == 'EOS':
				min_id = k

		return result_candidates[min_id]

