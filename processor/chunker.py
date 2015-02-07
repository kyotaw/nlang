# -*- coding: utf-8 -*-

import sys
import os
import pickle
from nlang.base.data.clause import Clause
from nlang.base.data.conn_table import ConnectivityTable
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
            self.__clauses = Clause(clause_file)
            conn_file = env.trained_clause_iob_connfile_path()
            if not os.path.exists(conn_file):
                conn_file = env.clause_iob_connfile_path()
            self.__iob_conn = ConnectivityTable(conn_file)
            self.__bos_clause = self.__clauses.clause(pos='BOS', clause='O')
            self.__eos_clause = self.__clauses.clause(pos='EOS', clause='O')
            self._Singleton__initialized = True

    def clause(self, tagged_words):
        return self.__interpret(self.__clause(tagged_words, self.__get_clause_cost_func(), self.__get_conn_cost_func()), 'lemma')

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
        
        node_list = self.__extract_clause_paths(pos_list)
        eos_node = self.__shortest_path_vitervi(node_list, len(pos_list), clause_cost_func, conn_cost_func)
        if not eos_node:
            return []
                
        return self.__summarize(eos_node, tagged_words)

    def __extract_clause_paths(self, pos_list):
        bos_node = {'clause':self.__bos_clause, 'total_cost':0, 'prev':None, 'start_index':-1}
        start_node_list = {}
        end_node_list = {}
        end_node_list[0] = [bos_node]

        length = len(pos_list)
        for i in range(0, length + 1):
            if i not in end_node_list:
                continue

            if i < length:
                clauses = self.__clauses.extract_clauses(pos_list[i])
                if len(clauses) == 0:
                    clauses = [(pos_list[i], 'B', 10)]
            else:
                clauses = [self.__eos_clause]
                
            start_node_list[i] = []
            for clause in clauses:
                new_node = {'clause':clause, 'total_cost':0, 'prev':None, 'start_index':i}
                start_node_list[i].append(new_node)
                for left_node in end_node_list[i]:
                    left_iob = left_node['clause'][1]
                    right_iob = clause[1]
                    if True:#self.__iob_conn.is_connectable(left_iob, right_iob):
                        index = i + 1
                        if index not in end_node_list:
                            end_node_list[index] = []
                        if new_node not in end_node_list[index]:
                            end_node_list[index].append(new_node)
        
        return (start_node_list, end_node_list)

    def __shortest_path_vitervi(self, node_list, length, clause_cost_func, conn_cost_func):
        for i in range(length+1):
            start_nodes = node_list[0][i] if i in node_list[0] else []
            for right_node in start_nodes:
                end_nodes = node_list[1][i] if i in node_list[1] else []
                min_cost = sys.maxsize
                min_cost_nodes = []
                for left_node in end_nodes:
                    left_iob = left_node['clause'][1]
                    right_iob = right_node['clause'][1]
                    total_cost = left_node['total_cost'] + clause_cost_func(right_node) + conn_cost_func(left_node, right_node)
                                                
                    if total_cost < min_cost:
                        min_cost = total_cost
                        min_cost_nodes = [left_node]
                    elif total_cost == min_cost:
                        min_cost = total_cost
                        min_cost_nodes.append(left_node)
                        
                    if len(min_cost_nodes) > 0:
                        right_node['total_cost'] = min_cost
                        right_node['prev'] = min_cost_nodes[0]
                
        eos_index = length + 1
        if eos_index not in node_list[1]:
            print('can\'t claused' )
            return None
        return node_list[1][eos_index][0]
        
    def __get_clause_cost_func(self, answer_clause_list=None):
        if answer_clause_list:
            def get_clause_cost_with_penalty(node):
                pos = node['clause'][0]
                cost = node['clause'][2]
                if pos == 'BOS' or pos == 'EOS':
                    return cost
                answer_iob = answer_clause_list[node['start_index']][0]
                node_iob = node['clause'][1]
                return cost + self.__penalty if answer_iob == node_iob else cost
            return get_clause_cost_with_penalty
        else:
            def get_clause_cost(node):
                return node['clause'][2]
            return get_clause_cost
        
    def __get_conn_cost_func(self, answer_clause_list=None):
        if answer_clause_list:
            def get_conn_cost_with_penalty(left_node, right_node):
                left_pos = left_node['clause'][0]
                right_pos = right_node['clause'][0]
                left_iob = left_node['clause'][1]
                right_iob = right_node['clause'][1]
                cost = self.__iob_conn.cost(left_iob, right_iob)
                if left_pos == 'BOS' or left_pos == 'EOS' or right_pos == 'BOS' or right_pos == 'EOS':
                    return cost

                left_answer_iob = answer_clause_list[left_node['start_index']][0]
                right_answer_iob = answer_clause_list[right_node['start_index']][0]
                return cost + self.__penalty if left_answer_iob == left_iob and right_answer_iob == right_iob else cost
            return get_conn_cost_with_penalty
        else:
            def get_conn_cost(left_node, right_node):
                left_iob = left_node['clause'][1]
                right_iob = right_node['clause'][1]
                return self.__iob_conn.cost(left_iob, right_iob)
            return get_conn_cost
        
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
            if node['clause'][0] != 'EOS':
                start = node['start_index']
                result.insert(0, (node['clause'][1], tagged_words[start]))
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
