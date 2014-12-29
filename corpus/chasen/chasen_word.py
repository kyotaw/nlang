# -*- coding: utf-8 -*-

from nlang.corpus.chasen.chasen_type import ChasenTagTable
from nlang.corpus.chasen.chasen_type import ChasenInvertTable

class ChasenWord(object):

	def __init__(self, data):
		self.valid = False
		class_name = data.__class__.__name__		
		if class_name == 'str' or class_name == 'unicode':
			self.__init_from_rawstring(data)
		elif class_name == 'TaggedWord':
			self.__init_from_tagged_word(data)
			self.valid = True


	def __init_from_rawstring(self, raw):
		tokens = raw[:-1].split('\t')
		if (len(tokens) < 4):
			return
		
		self.__lemma = tokens[0]
		self.__pron = tokens[1]
		self.__base = tokens[2]
		parts = tokens[3].split('-')
		self.__parts = (p for p in parts)
		if (len(tokens) > 4):
			self.__conj_form = tokens[4]
		else:
			self.__conj_form = ''
			self.__conj_type = ''
		if (len(tokens) > 5):
			self.__conj_type = tokens[5]
		else:
			self.__conj_type = ''
		
		self.valid = True
	
	def __init_from_tagged_word(self, tagged_word):
		self.__lemma = tagged_word['lemma']	
		self.__pron = tagged_word['pron']
		self.__base = tagged_word['base']
		tagged_form = tagged_word['conj_form']
		self.__conj_form = ChasenInvertTable[tagged_form] if tagged_form in ChasenInvertTable else ''
		tagged_type = tagged_word['conj_type']
		self.__conj_type = ChasenInvertTable[tagged_type] if tagged_type in ChasenInvertTable else ''
		pos_tokens = tagged_word['pos'].split('-')
		self.__parts = (ChasenInvertTable[p] for p in pos_tokens if p != tagged_form and p != tagged_type)
		
	def lemma(self, format='chasen'):
		return self.__lemma

	def pron(self, format='chasen'):
		return self.__pron

	def base(self, format='chasen'):
		return self.__base

	def pos(self, format='chasen'):
		if format == 'chasen':
			return self.__parts
		elif format == 'nlang':
			tag = ''
			for p in self.__parts:
				if tag:
					tag = tag + '-'
				tag = tag + ChasenTagTable[p]

			if self.__conj_form:
				if self.__conj_form in ChasenTagTable:
					tag += '-' + ChasenTagTable[self.__conj_form]
				else:
					print('NOT FOUND FORM IN TAGTABLE: ' + self.__conj_form)
					quit()
			if self.__conj_type:
				if self.__conj_type in ChasenTagTable:
					tag += '-' + ChasenTagTable[self.__conj_type]
				else:
					print('NOT FOUND TYPE IN TAGTABLE: ' + self.__conj_type)
					quit()
			return tag
		else:
			return ''
	
	def conj_form(self, format='chasen'):
		if format == 'chasen':
			return self.__conj_form
		elif format == 'nlang':
			return ChasenTagTable[self.__conj_form] if self.__conj_form in ChasenTagTable else ''
		else:
			return ''

	def conj_type(self, format='chasen'):
		if format == 'chasen':
			return self.__conj_type
		elif format == 'nlang':
			return ChasenTagTable[self.__conj_type] if self.__conj_type in ChasenTagTable else ''
		else:
			return ''
