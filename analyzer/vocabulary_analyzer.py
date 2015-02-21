from nlang.base.data.trie import Trie
from nlang.base.data.tagged_word import TaggedWord


class VocabularyAnalyzer:
    def __init__(self):
        self._tag_count = {}
        self._lemma_tag_count = Trie()

    def analyze(self, tagged_words):
        for word in tagged_words:
            if word.tag in self._tag_count:
                self._tag_count[word.tag] += 1
            else:
                self._tag_count[word.tag] = 1
            self._lemma_tag_count.insert(word.lemma, word.tag)

    def probability(self, lemma, tag):
        if tag not in self._tag_count:
            return 0.0
        return self._lemma_tag_count.count(lemma, tag) * 1.0 / self._tag_count[tag]
