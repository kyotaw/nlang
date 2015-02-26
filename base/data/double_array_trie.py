# -*- coding: utf-8 -*-

class DoubleArrayTrie(object):
    def __init__(self, size=1000):
        self._base = [-1] * size
        self._check = [-1] * size
        self._data = [None] * size
        self._size = size
        self._char_id_map = {}
        self._next_char_id = 1
    
    def insert(self, key, value):
        parent = 0      
        for key_head in key:
            child = self._traverse(parent, key_head)
            if child != -1:
                parent = child
                continue

            for i in range(parent + 1, self._size):
                if self._base[i] < 0 and self._check[i] < 0:
                    if key_head not in self._char_id_map:
                        self._char_id_map[key_head] = self._next_char_id
                        self._next_char_id += 1
                    self._base[parent] = i - self._char_id_map[key_head]
                    self._check[i] = parent
                    parent = i
                    break

        if self._data[parent] is None:
            self._data[parent] = value
    
    def common_prefix_search(self, key):
        res = []
        parent = 0
        for key_head in key:
            if self._data[parent] is not None:
                res.append(self._data[parent])

            child = self._traverse(parent, key_head)
            if child == -1:
                break
            parent = child
        return res

    def _traverse(self, parent, key_head):
        if key_head not in self._char_id_map:
            return -1 
        child = self._base[parent] + self._char_id_map[key_head]
        return child if self._check[child] == parent else -1
            
