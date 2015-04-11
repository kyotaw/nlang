import math

import numpy


class TfIdfWeight(object):
    def __init__(self, axes, term_freq_dic, doc_num, doc_num_per_term):
        self._axes = axes
        self._term_freq_dic = term_freq_dic
        self._doc_num = doc_num
        self._doc_num_per_term = doc_num_per_term
        self._term_freq_sum = sum(term_freq_dic.values())

    def weight(self, i):
        return self._tf(i) * self._idf(i)

    def _tf(self, i):
        term = self._axes[i]
        freq = self._term_freq_dic[term] if term in self._term_freq_dic else 0
        return freq / self._term_freq_sum

    def _idf(self, i):
        term = self._axes[i]
        return math.log2(self._doc_num / self._doc_num_per_term[term]) + 1
        

class DocVector(object):
    def __init__(self, axes, weighter):
        self._vector = numpy.array((weighter.weight(i) for i in range(self._axes)))

        
        
    
