# -*- coding: utf-8 -*-

from nlang.corpus.chasen.chasen_word import ChasenWord

class JugoWord(ChasenWord):
	def __init__(self, data):
		self.valid = True
		
		class_name = data.__class__.__name__		
		if class_name == 'str' or class_name == 'unicode':
			self.valid = self.init_from_rawstring(data)
		elif class_name == 'TaggedWord':
			self.valid = self.init_from_tagged_word(data)

	def init_from_rawstring(self, raw):
		res = super(JugoWord, self).init_from_rawstring(raw)
		if res == False:
			return False

		tokens = raw[:-1].split('\t')
		if len(tokens) == 5:
			self.__phrase = tokens[4]
		elif  len(tokens) == 7:
			self.__phrase = tokens[6]
		else:
			self.__phrase = 'O'
		
		return True

	def lemma(self, format='chasen'):
		return super(JugoWord, self).lemma(format)

	def pron(self, format='chasen'):
		return super(JugoWord, self).pron(format)

	def base(self, format='chasen'):
		return super(JugoWord, self).base(format)

	def pos(self, format='chasen'):
		return super(JugoWord, self).pos(format)
	
	def conj_form(self, format='chasen'):
		return super(JugoWord, self).conj_form(format)
	
	def conj_type(self, format='chasen'):
		return super(JugoWord, self).conj_type(format)
	
	def phrase(self, format='jugo'):
		return self.__phrase

			
