# -*- encoding: utf-8 -*-

import sys


class CostMinimizationMethod(object):
    def __init__(self, vocabulary, connection, loose_conn=True):
        self._vocab = vocabulary
        self._conn = connection
        self.loose_conn = loose_conn
        self._granularity = -1

    def extract_paths(self, data_stream):
        bos_node = {'data': self._vocab.get_bos(), 'total_cost': 0, 'prev': None, 'start_index': -1}
        start_node_list = {}
        end_node_list = {}
        end_node_list[0] = [bos_node]

        length = len(data_stream)
        for i in range(0, length + 1):
            if i not in end_node_list:
                continue

            if i < length:
                chunks = self._vocab.extract_vocabulary(self._get_data_grain(data_stream, i))
            else:
                chunks = [self._vocab.get_eos()]

            start_node_list[i] = []
            for chunk in chunks:
                new_node = {'data': chunk, 'total_cost': 0, 'prev': None, 'start_index': i}
                start_node_list[i].append(new_node)
                for left_node in end_node_list[i]:
                    left_hook = left_node['data'].get_hook()
                    right_hook = chunk.get_hook()
                    if self.loose_conn or self.__iob_conn.is_connectable(left_iob, right_iob):
                        index = i + chunk.get_length()
                        if index not in end_node_list:
                            end_node_list[index] = []
                        if new_node not in end_node_list[index]:
                            end_node_list[index].append(new_node)

        return (start_node_list, end_node_list)

    def shortest_path_vitervi(self, node_list, length, occurr_cost_func=None, conn_cost_func=None):
        start_node_list = node_list[0]
        end_node_list = node_list[1]
        for i in range(length + 1):
            start_nodes = start_node_list[i] if i in start_node_list else []
            for right_node in start_nodes:
                end_nodes = end_node_list[i] if i in end_node_list else []
                min_cost = sys.maxsize
                min_cost_nodes = []
                for left_node in end_nodes:
                    occurr_cost = occurr_cost_func(right_node) if occurr_cost_func else self._occurr_cost(right_node)
                    conn_cost = self._conn_cost(left_node, right_node)
                    total_cost = left_node['total_cost'] + occurr_cost + conn_cost

                    if total_cost < min_cost:
                        min_cost = total_cost
                        min_cost_nodes = [left_node]
                    elif total_cost == min_cost:
                        min_cost = total_cost
                        min_cost_nodes.append(left_node)

                if len(min_cost_nodes) > 0:
                    right_node['total_cost'] = min_cost
                    max_len = -1
                    for min_node in min_cost_nodes:
                        l = left_node['data'].get_length() + right_node['data'].get_length()
                        if max_len < l:
                            max_len = l
                            right_node['prev'] = min_node

        eos_index = length + 1
        if eos_index not in end_node_list:
            raise Exception('can\'t claused')
        return end_node_list[eos_index][0]

    def _occurr_cost(self, node):
        return node['data'].cost

    def _conn_cost(self, left_node, right_node):
        return self._conn.cost(left_node['data'].get_hook(), right_node['data'].get_hook())

    def _get_granularity(self):
        return self._granularity

    def _set_granularity(self, value):
        self._granularity = value

    granularity = property(_get_granularity, _set_granularity)

    def _get_data_grain(self, data_stream, start_index):
        if self.granularity <= 0:
            return data_stream[start_index:]
        elif len(data_stream) <= start_index + self.granularity:
            return data_stream[start_index:]
        elif self.granularity > 1:
            return data_stream[start_index:start_index + self.granularity]
        else:  # granularity == 1
            return data_stream[start_index]
