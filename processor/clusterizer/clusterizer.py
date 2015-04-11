import math
import sys

import numpy

from nlang.base.data.trie import Trie
from nlang.processor.clusterizer.doc_vector import TfIdfWeight

class Clusterizer(object):
    def __init__(self):
        self._terms = set()
        self._docs = {}
        self._doc_num_per_term = {}

    def add_document(self, tagged_words, doc_id):
        terms = {}
        for word in tagged_words:
            if word.tag.startswith('N-'):
                self._terms.add(word.lemma)
                if word.lemma not in terms:
                    terms[word.lemma] = 1
                else:
                    terms[word.lemma] += 1

        for term in terms:
            if term not in self._doc_num_per_term:
                self._doc_num_per_term[term] = 1
            else:
                self._doc_num_per_term[term] += 1
        self._docs[doc_id] = terms

    def clusterize(self, cluster_num=1):
        clusters = []

        axes = list(self._terms)
        axes.sort()
        for doc_id, doc_terms in self._docs.items():
            weighter = TfIdfWeight(axes, doc_terms, len(self._docs), self._doc_num_per_term)
            vals = []
            for i in range(len(axes)):
                vals.append(weighter.weight(i))
            doc_vec = numpy.array(vals)
            clusters.append([[doc_id, doc_vec]])
       
        while cluster_num < len(clusters):
            sim_cluster_index_pair = self._max_sim_clusters(clusters)
            clusters[sim_cluster_index_pair[0]].extend(clusters[sim_cluster_index_pair[1]])
            del clusters[sim_cluster_index_pair[1]]

        for cluster in clusters:
            for doc in cluster:
                del doc[1]

        return clusters
                
    def _max_sim_clusters(self, clusters):
        max_sim = -1
        max_sim_clusters = [0, 0]
        for i in range(len(clusters)):
            for j in range(i + 1, len(clusters)):
                sim = self._min_similality(clusters[i], clusters[j])
                if max_sim < sim:
                    max_sim = sim
                    max_sim_clusters = [i, j]
        return max_sim_clusters
    
    def _min_similality(self, cluster_a, cluster_b):
        min_sim = sys.maxsize
        for doc_a in cluster_a:
            for doc_b in cluster_b:
                sim = numpy.dot(doc_a[1], doc_b[1]) / (numpy.linalg.norm(doc_a[1]) * numpy.linalg.norm(doc_b[1]))
                if sim < min_sim:
                    min_sim = sim
        return min_sim

    def _max_similality(self, cluster_a, cluster_b):
        max_sim = -1
        for doc_a in cluster_a:
            for doc_b in cluster_b:
                sim = numpy.dot(doc_a[1], doc_b[1]) / (numpy.linalg.norm(doc_a[1]) * numpy.linalg.norm(doc_b[1]))
                if max_sim < sim:
                    max_sim = sim
        return max_sim

