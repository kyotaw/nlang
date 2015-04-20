import math
import sys
import random

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

    def clusterize(self, cluster_num=1, method='agglomerative'):
        doc_vectors = []
        axes = list(self._terms)
        axes.sort()
        for doc_id, doc_terms in self._docs.items():
            weighter = TfIdfWeight(axes, doc_terms, len(self._docs), self._doc_num_per_term)
            vals = []
            for i in range(len(axes)):
                vals.append(weighter.weight(i))
            doc_vec = numpy.array(vals)
            doc_vectors.append([doc_id, doc_vec])
     
        if method == 'agglomerative':
            clusters = self._agglomerative_clustering(doc_vectors, cluster_num)
        elif method == 'kmean':
            clusters = self._k_mean_clustering(doc_vectors, cluster_num)

        for cluster in clusters:
            for doc in cluster:
                del doc[1]

        return clusters

    def _k_mean_clustering(self, doc_vectors, cluster_num):
        if len(doc_vectors) == 0 or cluster_num <= 0:
            return None
        
        clusters = []
        for i in range(cluster_num):
            clusters.append([])
        cluster_index_list = []
        for doc in doc_vectors:
            cluster_index = random.randrange(0, cluster_num)
            cluster_index_list.append(cluster_index)
            clusters[cluster_index].append(doc)
        dimention = doc_vectors[0][1].shape[0]
        mean_vectors = []
        for i in range(cluster_num):
            mean_vectors.append(self._calc_mean_vector([doc[1] for doc in clusters[i]], dimention))
            
        transition = True
        while transition:
            new_clusters = []
            for i in range(cluster_num):
                new_clusters.append([])
            transition = False
            for i in range(len(doc_vectors)):
                doc = doc_vectors[i]
                max_sim_cluster = self._max_sim_cluster(doc[1], mean_vectors)
                new_clusters[max_sim_cluster].append(doc)
                if cluster_index_list[i] != max_sim_cluster:
                    cluster_index_list[i] = max_sim_cluster
                    transition = True

            if transition:
                for i in range(cluster_num):
                    mean_vectors[i] = self._calc_mean_vector([doc[1] for doc in new_clusters[i]], dimention)
                clusters = new_clusters

        return clusters
                
    def _max_sim_cluster(self, doc, mean_vectors):
        max_sim = -1
        max_sim_cluster = 0
        for i in range(len(mean_vectors)):
            mean_vec = mean_vectors[i]
            sim = numpy.dot(doc, mean_vec) / (numpy.linalg.norm(doc) * numpy.linalg.norm(mean_vec))
            if max_sim < sim:
                max_sim = sim
                max_sim_cluster = i

        return max_sim_cluster

    def _calc_mean_vector(self, vectors, dimention):
        sum_vec = numpy.array([0.0] * dimention)
        if len(vectors) == 0:
            return sum_vec
        for vec in vectors:
            sum_vec += vec
        return sum_vec / len(vectors)
               
    def _agglomerative_clustering(self, doc_vectors, cluster_num):
        clusters = [[doc] for doc in doc_vectors]
        while cluster_num < len(clusters):
            sim_cluster_index_pair = self._max_sim_cluster_pair(clusters)
            clusters[sim_cluster_index_pair[0]].extend(clusters[sim_cluster_index_pair[1]])
            del clusters[sim_cluster_index_pair[1]]
        
        return clusters

    def _max_sim_cluster_pair(self, clusters):
        max_sim = -1
        max_sim_cluster_pair = [0, 0]
        for i in range(len(clusters)):
            for j in range(i + 1, len(clusters)):
                sim = self._min_similality(clusters[i], clusters[j])
                if max_sim < sim:
                    max_sim = sim
                    max_sim_cluster_pair = [i, j]
        return max_sim_cluster_pair
    
    def _min_similality(self, doc_vectors_a, doc_vectors_b):
        min_sim = sys.maxsize
        for i in range(len(doc_vectors_a)):
            doc_a = doc_vectors_a[i]
            for j in range(len(doc_vectors_b)):
                doc_b = doc_vectors_b[j]
                sim = numpy.dot(doc_a[1], doc_b[1]) / (numpy.linalg.norm(doc_a[1]) * numpy.linalg.norm(doc_b[1]))
                if sim < min_sim:
                    min_sim = sim
        return min_sim

    def _max_similality(self, doc_vectors_a, doc_vectors_b):
        max_sim = -1
        for i in range(len(doc_vectors_a)):
            doc_a = doc_vectors_a[i]
            for j in range(len(doc_vectors_b)):
                doc_b = doc_vectors_b[j]
                sim = numpy.dot(doc_a[1], doc_b[1]) / (numpy.linalg.norm(doc_a[1]) * numpy.linalg.norm(doc_b[1]))
                if max_sim < sim:
                    max_sim = sim
        return max_sim

