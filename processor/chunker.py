# -*- coding: utf-8 -*-

import sys
import os
import pickle

import bz2

from nlang.base.data.clause import ClauseVocabulary
from nlang.base.data.conn_table import ConnectivityTable
from nlang.analyzer.cost_minimization_method import CostMinimizationMethod
from nlang.base.system import env
from nlang.base.util.singleton import Singleton


def Chunker(plain=False):
    def create_new_instance(cls):
        pickls = env.ready_made_chunker()
        if os.path.exists(pickls):
            with open(pickls, 'rb') as f:
                return pickle.loads(bz2.decompress(f.read()))
        return super(Singleton, cls).__new__(cls)
    return ChunkerImpl(None if plain else create_new_instance)


class ChunkerImpl(Singleton):
    _penalty = 1
    _eta = 1

    def __init__(self, new_instance_func):
        if not self._initialized:
            clause_file = env.trained_clausefile_path()
            if not os.path.exists(clause_file):
                clause_file = env.clausefile_path()
            self._clauses = ClauseVocabulary(clause_file)
            conn_file = env.trained_clause_iob_connfile_path()
            if not os.path.exists(conn_file):
                conn_file = env.clause_iob_connfile_path()
            self._iob_conn = ConnectivityTable(conn_file)
            self._analyzer = CostMinimizationMethod(self._clauses, self._iob_conn)
            self._analyzer.granularity = 1

            self._initialized = True

    def clause(self, tagged_words):
        return self._interpret(self._clause(tagged_words, None, None))

    def train(self, tagged_words, answer_claused_words):
        answer_clause_list = [(word[0], word[1].tag) for word in answer_claused_words]

        result_words = self._clause(tagged_words, self._get_clause_cost_func(answer_clause_list), self._get_conn_cost_func(answer_clause_list))

        result_clause_list = [(word[0], word[1].tag) for word in result_words]

        match = result_clause_list == answer_clause_list
        if not match:
            for i in range(len(result_clause_list)):
                answer = answer_clause_list[i]
                result = result_clause_list[i]
                if result != answer:
                    right = self._clauses.get(answer[1], answer[0])
                    right[2] -= 1
                    wrong = self._clauses.get(result[1], result[0])
                    wrong[2] += 1
                    if i != 0:
                        right_cost = self._iob_conn.cost(answer_clause_list[i - 1][0], answer[0])
                        self._iob_conn.set_cost(answer_clause_list[i - 1][0], answer[0], right_cost - 1)
                        wrong_cost = self._iob_conn.cost(result_clause_list[i - 1][0], result[0])
                        self._iob_conn.set_cost(result_clause_list[i - 1][0], result[0], wrong_cost + 1)

        self._regularize_l1()
        return match

    def _clause(self, tagged_words, clause_cost_func, conn_cost_func):
        pos_list = []
        for word in tagged_words:
            pos_list.append(word.tag)

        node_list = self._analyzer.extract_paths(pos_list)
        eos_node = self._analyzer.shortest_path_vitervi(node_list, len(pos_list), clause_cost_func, conn_cost_func)
        if not eos_node:
            return []

        return self._summarize(eos_node, tagged_words)

    def _get_clause_cost_func(self, answer_clause_list):
        def get_clause_cost_with_penalty(node):
            clause = node['data']
            cost = node['data'].cost
            if clause.is_bos or clause.is_eos:
                return cost
            answer_iob = answer_clause_list[node['start_index']][0]
            node_iob = clause.get_value()[1]
            return cost + self._penalty if answer_iob == node_iob else cost
        return get_clause_cost_with_penalty

    def _get_conn_cost_func(self, answer_clause_list):
        def get_conn_cost_with_penalty(left_node, right_node):
            left_clause = left_node['data']
            right_clause = right_node['data']
            left_iob = left_clause.value()[1]
            right_iob = right_clause.value()[1]
            cost = self._iob_conn.cost(left_iob, right_iob)
            if left_clause.is_bos or left_clause.is_eos or right_clause.is_bos or right_clause.is_eos:
                return cost

            left_answer_iob = answer_clause_list[left_node['start_index']][0]
            right_answer_iob = answer_clause_list[right_node['start_index']][0]
            return cost + self._penalty if left_answer_iob == left_iob and right_answer_iob == right_iob else cost
        return get_conn_cost_with_penalty

    def _regularize_l1(self):
        def regularize(cost, eta):
            if cost > 0:
                if cost - eta > 0:
                    cost -= eta
                else:
                    cost = 0
            else:
                if cost + eta < 0:
                    cost += eta
                else:
                    cost = 0
            return cost

        for pos, clause in self._clauses.dump():
            clause[2] = regularize(clause[2], self._eta)

        for conn in self._iob_conn.dump():
            self._iob_conn.set_cost(conn[0], conn[1], regularize(conn[2], self._eta))

    def _summarize(self, eos_node, tagged_words):
        result = []
        node = eos_node['prev']
        while node['prev']:
            start = node['start_index']
            result.insert(0, (node['data'].get_value()[1], tagged_words[start]))
            node = node['prev']
        return result

    def _interpret(self, claused_words):
        ret_clause_list = []
        feature_list = []
        prev_iob = ''
        for i in range(len(claused_words)):
            word = claused_words[i]
            iob_clause = word[0].split('-')
            f = word[1]
            if iob_clause[0] == 'O':
                if prev_iob == 'B' or prev_iob == 'I':
                    if len(feature_list) > 0:
                        ret_clause_list.append(feature_list)
                        feature_list = []
                ret_clause_list.append([f])
            elif iob_clause[0] == 'B':
                if prev_iob == 'B' or prev_iob == 'I':
                    if len(feature_list) > 0:
                        ret_clause_list.append(feature_list)
                feature_list = [f]
            elif iob_clause[0] == 'I':
                if prev_iob == 'B' or prev_iob == 'I':
                    feature_list.append(f)
            prev_iob = iob_clause[0]

        if prev_iob == 'B' or prev_iob == 'I':
            if len(feature_list) > 0:
                ret_clause_list.append(feature_list)

        return ret_clause_list
