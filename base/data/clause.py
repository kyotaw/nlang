# -*- coding: utf-8 -*-

from nlang.base.data.trie import Trie

class Clause(object):
    def __init__(self, raw_clause):
        self.__raw = raw_clause
    
    def get_value(self):
        return self.__raw

    def get_hook(self):
        return self.__raw[1]
    
    def get_length(self):
        return 1

    def is_bos(self):
        return True if self.__raw[0] == 'BOS' else False

    def is_eos(self):
        return True if self.__raw[0] == 'EOS' else False
       
    def _get_cost(self):
        return self.__raw[2]

    def _set_cost(self, value):
        self.__raw[2] = value

    cost = property(_get_cost, _set_cost)

class ClauseVocabulary(object):

    def __init__(self, file_path):
        self.__clauses = Trie()
        self.__clauses.insert('BOS', ['BOS', 'O', 0])
        self.__clauses.insert('EOS', ['EOS', 'O', 0])

        with open(file_path, 'r') as f:
            line = f.readline()
            while line:
                tokens = line[:-1].split('\t')
                if len(tokens) < 3:
                    continue
                pos = tokens[0]
                self.__clauses.insert(pos, [pos, tokens[1], int(tokens[2])])
                line = f.readline()


    def extract_vocabulary(self, pos):
        ret = [Clause(raw_clause) for raw_clause in self.__clauses.get(pos)]
        if len(ret) == 0:
            ret = [Clause([pos, 'O', 10])]
        return ret

    def get_bos(self):
        return self.__get_clause('BOS', 'O') 
    
    def get_eos(self):
        return self.__get_clause('EOS', 'O') 

    def dump(self):
        return self.__clauses.dump()

    def __get_clause(self, pos, iob):
        not_found = Clause(['', '', 0])
        cands = self.__clauses.get(pos)
        for p in cands:
            if iob == p[1]:
                return Clause(p)
        return not_found
