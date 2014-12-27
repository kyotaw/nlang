from nlang.base.data.trie import Trie

class VocabularyAnalyzer:
	def __init__(self):
		self.pos_count = {}
		self.morp_count = Trie()

	def analyze(self, tagged_words):
		for word in tagged_words:
			if word[2] in self.pos_count:
				self.pos_count[word[2]] += 1
			else:
				self.pos_count[word[2]] = 1

			self.morp_count.insert(word[0], word[2])

	def probability(self, morp, pos):
		if pos not in self.pos_count:
			return 0
		return self.morp_count.count(morp, pos) * 1.0 / self.pos_count[pos]	
		
