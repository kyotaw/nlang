# -*- coding: utf-8 -*-

from nlang.base.data.conn_table import ConnectivityTable
from nlang.base.data.vocabulary import Vocabulary
from nlang.base.util.util import pp
from nlang.base.system import env
import sys

class Tokenizer(object):
	def __init__(self):
		self.__conn_table = ConnectivityTable(env.connfile_path())
		self.__vocab = Vocabulary(env.vocabfile_path())
		self.__bos_word = self.__vocab.word(lemma='BOS', pos='BOS')
		self.__eos_word = self.__vocab.word(lemma='EOS', pos='EOS')
	
	def tag(self, sentence):
		return self.__parse(sentence)

	def __parse(self, sentence):
		bos_node = {'word':self.__bos_word, 'total_cost':0, 'prev':None}
		node_list = {}
		node_list[0] = [bos_node]

		length = len(sentence)
		for i in range(0, length + 1):
			if i not in node_list:
				continue

			if i < length:
				words = self.__vocab.extract_words(sentence[i:])
			else:
				words = [self.__eos_word]
			
			for word in words:
				new_node = {'word':word, 'total_cost':0, 'prev':None}
				min_cost = sys.maxint
				min_cost_nodes = []
				for left_node in node_list[i]:
					if self.__conn_table.is_connectable(left_node['word']['pos'], word['pos']):
						total_cost = left_node['total_cost'] + word['cost'] + self.__conn_table.cost(left_node['word']['pos'], word['pos'])
						
						if total_cost < min_cost:
							min_cost = total_cost
							min_cost_nodes = [left_node]
						elif total_cost == min_cost:
							min_cost = total_cost
							min_cost_nodes.append(left_node)
			
				if len(min_cost_nodes) > 0:
					new_node['total_cost'] = min_cost
					max_len = -1
					for left_node in min_cost_nodes:
						l = left_node['word']['length']	+ word['length']
						if max_len < l:
							max_len = l
							new_node['prev'] = left_node

					index = i + word['length']
					if index not in node_list:
						node_list[index] = []
					if new_node not in node_list[index]:
						node_list[index].append(new_node)
	
		result = []
		node = node_list[length+1][0] #EOS
		while node['prev']:
			result.insert(0, node['word'])
			node = node['prev']
		result.insert(0, node['word']) #BOS

		return result

