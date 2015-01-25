# -*- coding: utf-8 -*-

import sys
import os 
import pickle
from nlang.base.data.conn_table import ConnectivityTable
from nlang.base.data.vocabulary import Vocabulary
from nlang.processor.sentencer import Sentencer
from nlang.base.util.util import pp
from nlang.base.system import env

class Tokenizer(object):
        @classmethod
        def create(cls):
            pickls = env.ready_made_tokenizer()
            if os.path.exists(pickls):
                with open(pickls, 'rb') as f:
                    return pickle.load(f)
            return cls()
	
        def __init__(self):
		self.__conn_table = ConnectivityTable(env.connfile_path())
		self.__vocab = Vocabulary(env.vocabfile_path())
		self.__bos_word = self.__vocab.word(lemma='BOS', pos='BOS')
		self.__eos_word = self.__vocab.word(lemma='EOS', pos='EOS')
                self.__sentencer = Sentencer.create()
	
	def tag(self, stream):
            words = []
            for sent in self.__sentencer.sentences(stream):
                words += self.__parse(sent)
            return words

	def __parse(self, stream):
		bos_node = {'word':self.__bos_word, 'total_cost':0, 'prev':None}
		node_list = {}
		node_list[0] = [bos_node]

		length = len(stream)
		for i in range(0, length + 1):
			if i not in node_list:
				continue

			if i < length:
				words = self.__vocab.extract_words(stream[i:])
			else:
				words = [self.__eos_word]
			
			for word in words:
				new_node = {'word':word, 'total_cost':0, 'prev':None}
				min_cost = sys.maxint
				min_cost_nodes = []
				for left_node in node_list[i]:
                                    if True:#self.__conn_table.is_connectable(left_node['word']['pos'], word['pos']):
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
                eos_index = length + 1
                if eos_index not in node_list:
                    print('can\'t tagged : ' + stream.encode('utf_8'))
                    return result

		node = node_list[length+1][0]['prev'] #EOS
		while node['prev']:
			result.insert(0, node['word'])
			node = node['prev']

		return result
	
