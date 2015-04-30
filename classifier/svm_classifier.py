import numpy

# import matplotlib.pyplot as plt

from nlang.base.system import env
from nlang.base.data.trie import Trie
from nlang.base.data.vocabulary import WordVocabulary


class ObjectiveFunc_l1(object):
    def __init__(self, dimention):
        self._dimention = dimention
        self._step = 0.1
        self.weight_vec = numpy.ones(self._dimention)
        self.legularization_factor = 0.1

    def optimize(self, x, y):
        self._weight_vec -= self._step * self._grad(x, y)

    def _grad(self, x, y):
        # loss factor
        gloss = numpy.zeros(self._dimention)
        if self._weight_vec.dot(x) * y < 1.0:
            gloss += (x * y)

        # legularizaton facutor
        lloss = numpy.zeros(self._dimention)
        for w, i in enumrate(self._weight_vec):
            if 1.0e-15 < w:
                lloss[i] = self._legularization_factor * self._sign(w)

        return gloss + lloss

    def _sign(self, v):
        return 1.0 if 0 <= v else -1.0


class ObjectiveFunc(object):
    def __init__(self, n, dim):
        self._n = n
        self._dim = dim
        self._lagrange = numpy.zeros(n)
        self._learn_rate = 0.01
        self._support_vec_indexes = []
        self._weight_vec = numpy.zeros(dim + 1)

    def evaluate(self, doc_vector):
        return self._weight_vec[:self._dim].dot(doc_vector) - self._weight_vec[self._dim]

    def f(self, x):
        b = self._weight_vec[self._dim]
        return (-1.0 * self._weight_vec[0] / self._weight_vec[1] * x) + (b / self._weight_vec[1])

    def optimize(self, doc_vectors, labels):
        self._support_vec_indexes = []
        self._weight_vec = numpy.zeros(self._dim + 1)
        for i in range(self._n):
            new_val = self._lagrange[i] + self._learn_rate * self._grad(i, doc_vectors, labels)
            if new_val < 0:
                new_val = 0
            if 1.0e-15 < new_val:
                self._support_vec_indexes.append(i)
                self._weight_vec += new_val * labels[i] * doc_vectors[i]

            self._lagrange[i] = new_val

    def _grad(self, i, doc_vectors, labels):
        sum_ = 0
        for j in range(self._n):
            sum_ += self._lagrange[j] * labels[i] * labels[j] * self._kernel(doc_vectors[i], doc_vectors[j])
        return 1 - sum_

    def _kernel(self, vec_1, vec_2):
        return vec_1.dot(vec_2)


class SVMClassifier(object):
    def __init__(self):
        vocab = WordVocabulary(env.vocabfile_path())
        self._word_id_map = Trie()
        self._dim = 0
        for word in vocab.get_all_words():
            if word.pos[0] in ['N', 'V']:
                self._word_id_map.insert(word.lemma, self._dim)
                self._dim += 1
        self._obj_func = None

    def classify(self, tagged_words):
        if not self._obj_func:
            return 1
        word_freq = self._vectorize(tagged_words)
        val = self._obj_func.evaluate(numpy.array(word_freq))
        return -1 if val < 0 else 1

    def train(self, data_list, train_count=1000):
        doc_vectors = []
        labels = []
        for data in data_list:
            tagged_words = data[0]
            word_freq = self._vectorize(tagged_words)
            doc_vector = numpy.array(word_freq + [1])
            doc_vectors.append(doc_vector)
            labels.append(data[1])

        n = len(data_list)
        self._obj_func = ObjectiveFunc(n, self._dim)
        for i in range(train_count):
            self._obj_func.optimize(doc_vectors, labels)

        # show
        # print(self._obj_func._lagrange)

        # for i in range(len(doc_vectors)):
        #     if labels[i] > 0:
        #         plt.plot(doc_vectors[i][0], doc_vectors[i][1], 'bx')
        #     else:
        #         plt.plot(doc_vectors[i][0], doc_vectors[i][1], 'rx')
        # for sv in self._obj_func._support_vec_indexes:
        #     plt.scatter(doc_vectors[sv][0], doc_vectors[sv][1], s=80, c='y', marker='o')

        # x1 = numpy.linspace(-6, 6, 1000)
        # x2 = [self._obj_func.f(x) for x in x1]
        # plt.plot(x1, x2, 'g-')

        # plt.xlim(-6, 6)
        # plt.ylim(-6, 6)

        # plt.savefig('svm.png')

    def _vectorize(self, tagged_words):
        word_freq = [0] * self._dim
        for word in tagged_words:
            if word.pos[0] in ['N', 'V']:
                word_id = self._word_id_map.get(word.lemma)
                if word_id:
                    word_freq[word_id[0]] += 1

        return word_freq
