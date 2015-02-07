# -*- coding: utf-8 -*-

import sys
from nlang.base.data.trie import Trie
from nlang.base.data.cost_calculator import calculate_cost

class NaiveBayesClassifier(object):
    def __init__(self):
        self.__feature_freq = {}
        self.__feature_vocabulary = {}
        self.__feature_count = {}
        self.__label_count = {}

    def train(self, data):
        data_list = None
        if isinstance(data, tuple):
            data_list = [data]
        elif isinstance(data, list):
            data_list = data
                
        if data_list:
            for data in data_list:
                label = data[0]
                feature = data[1]
                self.__add_label(label)
                self.__add_feature(feature, label)

    def classify(self, feature):
        min_cost = sys.maxsize
        better_label = ''
        for label in self.__label_count.keys():
            cost = calculate_cost(self.__probability_label(label) + self.__probability_feature(feature, label))
            if cost < min_cost:
                min_cost = cost
                better_label = label

        return better_label

    def informative_features(self, best_n):
        informatives_list = {}
        for label in self.__label_count.keys():
            informatives_list[label] = {}
            for feature_name in self.__feature_count[label].keys():
                informatives_list[label][feature_name] = []
                for feature_value_list, feature_label in self.__feature_freq[feature_name].dump():
                    feature_value = ''.join(feature_value_list)
                    if feature_label != label:
                        continue
                    prov = self.__probability_feature({feature_name:feature_value}, label)
                    informatives_list[label][feature_name].append((feature_value, prov))
                informatives_list[label][feature_name] = sorted(informatives_list[label][feature_name], key=lambda value: value[1])
                informatives_list[label][feature_name].reverse()
                informatives_list[label][feature_name] = informatives_list[label][feature_name][:best_n]
        return informatives_list

    def __probability_label(self, label):
        return self.__label_count[label] * 1.0 / sum(self.__label_count.values()) 

    def __probability_feature(self, feature, label):
        prob = 0.0
        for name, value in feature.items():
            feature_name = name
            if isinstance(value, list):
                for v in value:
                    feature_value = v
                    prob += self.__feature_freq[name].count(feature_value, label) * 1.0 / (self.__feature_count[label][feature_name] + len(self.__feature_vocabulary[feature_name]))
            else:
                feature_value = value
                prob += self.__feature_freq[feature_name].count(feature_value, label) * 1.0 / (self.__feature_count[label][feature_name] + len(self.__feature_vocabulary[feature_name]))
        return prob

    def __add_feature(self, feature, label):
        for name, value in feature.items():
            feature_name = name
            feature_value = value
            self.__set_dict_default(self.__feature_freq, feature_name, Trie())
            self.__set_dict_default(self.__feature_vocabulary, feature_name, set())
            self.__set_dict_default(self.__feature_count, label, {})
            self.__set_dict_default(self.__feature_count[label], feature_name, 0)

            if isinstance(feature_value, list): 
                for value in feature_value:
                    self.__feature_freq[feature_name].insert(value, label)
                    self.__feature_vocabulary[feature_name].add(value)
                    self.__feature_count[label][feature_name] += 1
            else:
                self.__feature_freq[feature_name].insert(feature_value, label)
                self.__feature_vocabulary[feature_name].add(feature_value)
                self.__feature_count[label][feature_name] += 1
                                
    def __add_label(self, label):
        self.__set_dict_default(self.__label_count, label, 0)
        self.__label_count[label] += 1

    def __set_dict_default(self, dic, key, default_value):
        if key not in dic:
            dic[key] = default_value
