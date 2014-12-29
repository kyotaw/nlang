# -*- coding: utf-8 -*-

class TaggedWord(object):

	def __init__(self, lemma='', pron='', base='', pos='', conj_form='', conj_type='', cost=0, length=0):
	
		self.__word = {
			'lemma':lemma,
			'pron':pron,
			'base':base,
			'pos':pos,
			'conj_form':conj_form,
			'conj_type':conj_type,
			'cost':cost,
			'length':length if length > 0 else len(lemma) 
		}

	def get(self):
		return (self.__word['lemma'], self.__word['pron'], self.__word['base'], self.__word['pos'])
	
	def __getitem__(self, key):
		return self.__word[key] if key in self.__word else ''

	def __eq__(self, other):
		return self.__word == other.__word

	def __ne__(self, other):
		return self.__word != other.__word

