# -*- coding: utf-8 -*-

from nlang.base.data.trie import Trie


class ClauseAnalyzer(object):
    def __init__(self):
        self._tag_iob_count = Trie()
        self._iob_count = {}
        self._iob_conn = Trie()

    def analyze(self, claused_words):
        prev_iob = 'O'
        self._add_iob_count(prev_iob)
        for i in range(len(claused_words)):
            iob = claused_words[i][0]
            tag = claused_words[i][1].tag
            self._tag_iob_count.insert(tag, iob)
            self._iob_conn.insert(prev_iob, iob)
            self._add_iob_count(iob)
            prev_iob = iob
            prev_tag = tag

        self._add_iob_count('O')
        self._iob_conn.insert(prev_iob, 'O')

    def calc_clause_probability(self):
        clause_list = []
        for tag_iob in self._tag_iob_count.dump():
            tag = tag_iob[0]
            iob = tag_iob[1]
            clause_list.append((''.join(tag), iob, self._tag_iob_count.count(tag, iob) * 1.0 / self._iob_count[iob]))
        return clause_list

    def calc_enter_conn_probability(self):
        conn_list = {}
        for conn in self._iob_conn.dump():
            left_iob = ''.join(conn[0])
            right_iob = conn[1]
            if left_iob not in conn_list:
                conn_list[left_iob] = []
            conn_list[left_iob].append((right_iob, self._iob_conn.count(left_iob, right_iob) * 1.0 / self._iob_count[left_iob]))
        return conn_list

    def _add_iob_count(self, iob):
        if iob in self._iob_count:
            self._iob_count[iob] += 1
        else:
            self._iob_count[iob] = 1
