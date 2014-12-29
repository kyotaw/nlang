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
		bos_node = {'next':[], 'entry':bos_entry, 'total_cost':0}
		node_list = {}
		node_list[0] = [bos_node]

		length = len(sentence)
		for i in range(0, length + 1):
			if i not in node_list:
				continue

			if i < length:
				entries = self.__vocab.extract_words(sentence[i:])
			else:
				entries = [eos_entry]

			for entry in entries:
				new_node = {'next':[], 'entry':entry, 'total_cost':0}
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
						left_node['next'].append(new_node)
				
					index = i + entry['length']
					if index not in node_list:
						node_list[index] = []
					if new_node not in node_list[index]:
						node_list[index].append(new_node)


		return self.__enum_nodes(bos_node, tagged)
	
	def __enum_nodes(self, node, tagged):
		stream_list = []
		lemma = node['entry']['lemma']
		if lemma == u'EOS':
			if tagged:
				return [[node['entry']]]
			else:
				return [[lemma]]
		
		if 'next' not in node or len(node['next']) == 0:
			return [[]]

		for	next_node in node['next']:
			sub_stream_list = self.__enum_nodes(next_node, tagged)
			for stream in sub_stream_list:
				if len(stream) > 0:
					stream_list.append([lemma] + stream)
		return stream_list


