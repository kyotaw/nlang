# -*- coding: utf-8 -*-

import sys
from nlang.base.data.trie import Trie
from nlang.base.data.cost_calculator import calculate_cost


class NaiveBayesClassifier(object):
    def __init__(self):
        self._feature_freq = {}
        self._feature_vocabulary = {}
        self._feature_count = {}
        self._label_count = {}

    def train(self, data):
        data_list = None
        if isinstance(data, tuple):
            data_list = [data]
        elif isinstance(data, list):
            data_list = data

        if data_list:
            for data in data_list:
                label = str(data[0])
                feature = data[1]
                self._add_label(label)
                self._add_feature(feature, label)

    def classify(self, feature):
        min_cost = sys.maxsize
        better_label = ''
        for label in self._label_count.keys():
            cost = calculate_cost(self._probability_label(label) + self._probability_feature(feature, label))
            if cost < min_cost:
                min_cost = cost
                better_label = label

        return better_label

    def informative_features(self, best_n):
        informatives_list = {}
        for label in self._label_count.keys():
            informatives_list[label] = {}
            for feature_name in self._feature_count[label].keys():
                informatives_list[label][feature_name] = []
                for feature_value_list, feature_label in self._feature_freq[feature_name].dump():
                    feature_value = ''.join(feature_value_list)
                    if feature_label != label:
                        continue
                    prov = self._probability_feature({feature_name: feature_value}, label)
                    informatives_list[label][feature_name].append((feature_value, prov))
                informatives_list[label][feature_name] = sorted(informatives_list[label][feature_name], key=lambda value: value[1])
                informatives_list[label][feature_name].reverse()
                informatives_list[label][feature_name] = informatives_list[label][feature_name][:best_n]
        return informatives_list

    def evaluate(self, test_data_list):
        unique_label_list = set()
        answer_label_list = []
        test_label_list = []
        for test_data in test_data_list:
            label = test_data[0]
            feature = test_data[1]
            unique_label_list.add(label)
            answer_label_list.append(label)
            test_label_list.append(self.classify(feature))

        precision_list = []
        recall_list = []
        f_list = []
        for label in unique_label_list:
            true_positive = 0
            for i in range(len(answer_label_list)):
                if label == answer_label_list[i] and answer_label_list[i] == test_label_list[i]:
                    true_positive += 1

            precision = true_positive / test_label_list.count(label)
            recall = true_positive / answer_label_list.count(label)
            precision_list.append(precision)
            recall_list.append(recall)
            f_list.append(2 * precision * recall / (precision + recall))
        
        return {
            'precision': sum(precision_list) / len(precision_list),
            'recall': sum(recall_list) / len(recall_list),
            'f': sum(f_list) / len(f_list)
        }

    def _probability_label(self, label):
        return self._label_count[label] * 1.0 / sum(self._label_count.values())

    def _probability_feature(self, feature, label):
        prob = 0.0
        for name, value in feature.items():
            feature_name = name
            if isinstance(value, list):
                for v in value:
                    feature_value = v
                    prob += self._feature_freq[name].count(feature_value, label) * 1.0 / (self._feature_count[label][feature_name] + len(self._feature_vocabulary[feature_name]))
            else:
                feature_value = value
                prob += self._feature_freq[feature_name].count(feature_value, label) * 1.0 / (self._feature_count[label][feature_name] + len(self._feature_vocabulary[feature_name]))
        return prob

    def _add_feature(self, feature, label):
        for name, value in feature.items():
            feature_name = name
            feature_value = value
            self._set_dict_default(self._feature_freq, feature_name, Trie())
            self._set_dict_default(self._feature_vocabulary, feature_name, set())
            self._set_dict_default(self._feature_count, label, {})
            self._set_dict_default(self._feature_count[label], feature_name, 0)

            if isinstance(feature_value, list):
                for value in feature_value:
                    self._feature_freq[feature_name].insert(value, label)
                    self._feature_vocabulary[feature_name].add(value)
                    self._feature_count[label][feature_name] += 1
            else:
                self._feature_freq[feature_name].insert(feature_value, label)
                self._feature_vocabulary[feature_name].add(feature_value)
                self._feature_count[label][feature_name] += 1

    def _add_label(self, label):
        self._set_dict_default(self._label_count, label, 1)
        # self._label_count[label] += 1

    def _set_dict_default(self, dic, key, default_value):
        if key not in dic:
            dic[key] = default_value
