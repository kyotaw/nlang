# -*- coding: utf-8 -*-

from nlang.base.data.trie import Trie
from nlang.base.data.tagged_word import TaggedWord
from nlang.base.util.util import *

class Vocabulary:
	def __init__(self, file_path):
		self.__words = Trie()
		
		self.__words.insert('BOS', TaggedWord(lemma='BOS', pron='BOS', pos='BOS', cost=0, length=1))
		self.__words.insert('EOS', TaggedWord(lemma='EOS', pron='EOS', pos='EOS', cost=0, length=1))

		with open(file_path, 'r') as f:
			line = f.readline()
			while line:
				tokens = line[:-1].split('\t')
				if len(tokens) < 5:
					continue
				
				word = TaggedWord(
					lemma=tokens[0].decode('utf-8'),
					pron=tokens[1].decode('utf-8'),
					base=tokens[2].decode('utf-8'),
					pos=tokens[3],
					cost=tokens[4],
					length=len(tokens[0].decode('utf-8'))
				)
				self.__words.insert(word['lemma'], word)
				line = f.readline()

	def word(self, lemma, pos):
		not_found = TaggedWord()
		cands = self.__words.common_prefix_search(lemma)
		for w in cands:
			if w['lemma'] == lemma and w['pos'] == pos:
				return w	
		return not_found
			
	def extract_words(self, stream):
		words = self.__words.common_prefix_search(stream)
		return words if len(words) > 0 else self.__assume_unknown_word(stream)
	
	def __assume_unknown_word(self, stream):
		length = len(stream)
		if length == 0:
			return []
		prev_type = '' 
		last_index = 0
		for i in range(length):
			char_type = get_char_type(stream[i])
			if prev_type != '' and prev_type != char_type:
				break
			prev_type = char_type
			last_index = i

		unk_word = stream[:last_index+1]
		tagged_word = TaggedWord(lemma=unk_word, pron='UNK', base='UNK', pos='UNK', cost='10', length=len(unk_word))
		return [tagged_word]

