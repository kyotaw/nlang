# -*- coding: utf-8 -*-

class ConnectivityAnalyzer:
	def __init__(self):
		self.connect_table = {}
		self.freq_table = {}
	
	def analyze(self, tagged_words):
		sentence = []
		for word in tagged_words:
			if word[2] == 'SY-PE':
				sentence.append(word[2])
				self.__analyze(sentence)
				del sentence[:]
			else:
				sentence.append(word[2])

		for k, v in self.freq_table.items():
			total = float(sum(v))
			def prob(item): return round(item / total, 3)
			self.freq_table[k] = map(prob, v)

	def __analyze(self, sentence):
		cur_left = u'BOS'
		for s in sentence:
			if cur_left not in self.connect_table:
				self.connect_table[cur_left] = []
				self.freq_table[cur_left] = []
			if s not in self.connect_table[cur_left]:
				self.connect_table[cur_left].append(s)
				self.freq_table[cur_left].append(1)
			else:
				self.freq_table[cur_left][self.connect_table[cur_left].index(s)] += 1
			cur_left = s
		if cur_left not in self.connect_table:
			self.connect_table[cur_left] = []
			self.freq_table[cur_left] = []
		if 'EOS' not in self.connect_table[cur_left]:
			self.connect_table[cur_left].append('EOS')
			self.freq_table[cur_left].append(1)
		else:
			self.freq_table[cur_left][self.connect_table[cur_left].index('EOS')] += 1
