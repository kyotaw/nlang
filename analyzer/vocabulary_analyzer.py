from nlang.base.data.trie import Trie
from nlang.base.data.tagged_word import TaggedWord

class VocabularyAnalyzer:
	def __init__(self):
		self.pos_count = {}
		self.morp_count = Trie()

	def analyze(self, tagged_words):
		for word in tagged_words:
			if word['pos'] in self.pos_count:
				self.pos_count[word['pos']] += 1
			else:
				self.pos_count[word['pos']] = 1

			self.morp_count.insert(word['lemma'], word['pos'])

	def probability(self, morp, pos):
		if pos not in self.pos_count:
			return 0
		return self.morp_count.count(morp, pos) * 1.0 / self.pos_count[pos]	
		
