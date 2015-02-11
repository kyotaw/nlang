

import sys
import os
import pickle
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
                return pickle.load(f)
        return super(Singleton, cls).__new__(cls)
    return ChunkerImpl(None if plain else create_new_instance)

class ChunkerImpl(Singleton):
    __penalty = 1
    __eta = 1

    def __init__(self, new_instance_func):
        if not self._Singleton__initialized:
            clause_file = env.trained_clausefile_path()
            if not os.path.exists(clause_file):
                clause_file = env.clausefile_path()
            self.__clauses = ClauseVocabulary(clause_file)
            conn_file = env.trained_clause_iob_connfile_path()
            if not os.path.exists(conn_file):
                conn_file = env.clause_iob_connfile_path()
            self.__iob_conn = ConnectivityTable(conn_file)
            self.__analyzer = CostMinimizationMethod(self.__clauses, self.__iob_conn)
            self.__analyzer.granularity = 1

            self._Singleton__initialized = True

    def clause(self, tagged_words):
        return self.__interpret(self.__clause(tagged_words, None, None), 'lemma')

    def train(self, tagged_words, answer_claused_words):
        answer_clause_list = [(word[0], word[1]['pos']) for word in answer_claused_words]

        result_words = self.__clause(tagged_words, self.__get_clause_cost_func(answer_clause_list), self.__get_conn_cost_func(answer_clause_list))
                
        result_clause_list = [(word[0], word[1]['pos']) for word in result_words]
                
        match = result_clause_list == answer_clause_list
        if not match:
            for i in range(len(result_clause_list)):
                answer = answer_clause_list[i]
                result = result_clause_list[i]
                if result != answer:
                    right = self.__clauses.clause(answer[1], answer[0])
                    right[2] -= 1
                    wrong = self.__clauses.clause(result[1], result[0])
                    wrong[2] += 1
                    if i != 0:
                        right_cost = self.__iob_conn.cost(answer_clause_list[i-1][0], answer[0])
                        self.__iob_conn.set_cost(answer_clause_list[i-1][0], answer[0], right_cost - 1)
                        wrong_cost = self.__iob_conn.cost(result_clause_list[i-1][0], result[0])
                        self.__iob_conn.set_cost(result_clause_list[i-1][0], result[0], wrong_cost + 1)
                
        self.__regularize_l1()
        return match

    def __clause(self, tagged_words, clause_cost_func, conn_cost_func):
        pos_list = []
        for word in tagged_words:
            pos_list.append(word['pos'])
        
        node_list = self.__analyzer.extract_paths(pos_list)
        eos_node = self.__analyzer.shortest_path_vitervi(node_list, len(pos_list), clause_cost_func, conn_cost_func)
        if not eos_node:
            return []
                
        return self.__summarize(eos_node, tagged_words)

    def __get_clause_cost_func(self, answer_clause_list):
        def get_clause_cost_with_penalty(node):
            pos = node['data'].get_hook()
            cost = node['data'].get_value()[1]
            if pos == 'BOS' or pos == 'EOS':
                return cost
            answer_iob = answer_clause_list[node['start_index']][0]
            node_iob = node['data'].get_value()[1]
            return cost + self.__penalty if answer_iob == node_iob else cost
        return get_clause_cost_with_penalty
        
    def __get_conn_cost_func(self, answer_clause_list):
        def get_conn_cost_with_penalty(left_node, right_node):
            left_pos = left_node['data'].get_hook()
            right_pos = right_node['data'].get_hook()
            left_iob = left_node['data'].value()[1]
            right_iob = right_node['data'].value()[1]
            cost = self.__iob_conn.cost(left_iob, right_iob)
            if left_node['data'].is_bos or left_node['data'].is_eos() == 'EOS' or right_node['data'].is_bos() or right_node['data'].is_eos():
                return cost

            left_answer_iob = answer_clause_list[left_node['start_index']][0]
            right_answer_iob = answer_clause_list[right_node['start_index']][0]
            return cost + self.__penalty if left_answer_iob == left_iob and right_answer_iob == right_iob else cost
        return get_conn_cost_with_penalty
        
    def __regularize_l1(self):
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

        for pos, clause in self.__clauses.dump():
            clause[2] = regularize(clause[2], self.__eta)

        for conn in self.__iob_conn.dump():
            self.__iob_conn.set_cost(conn[0], conn[1], regularize(conn[2], self.__eta))
                        
    def __summarize(self, eos_node, tagged_words):
        result = []
        node = eos_node
        while node['prev']:
            if not node['data'].is_eos():
                start = node['start_index']
                result.insert(0, (node['data'].get_value()[1], tagged_words[start]))
            node = node['prev']
        return result
        
    def __interpret(self, claused_words, feature):
        ret_clause_list = []
        feature_list = []
        prev_iob = ''
        for i in range(len(claused_words)):
            word = claused_words[i]
            iob_clause = word[0].split('-')
            f = word[1][feature] if feature else word[1]
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
