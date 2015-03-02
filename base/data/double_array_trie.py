# -*- coding: utf-8 -*-

class DoubleArrayTrie(object):
    def __init__(self, size=1000):
        self._base = []
        self._check = []
        self._codes = []
        self._data = []
        self._size = 0
        self._extend(size)
        for i in range(0, size):
            self._check[i] = -(i + 1)
        self._empty_node_head = 1

        self._code_map = {}
        self._next_code = 1
    
    def insert(self, key, value):
        found, index, key_pos = self._search(key)
        if not found:
            self._insert(index, key[key_pos:], value)
    
    def search(self, key):
        found, index, key_pos = self._search(key)
        return self._data[index] if found else None
    
    def common_prefix_search(self, key):
        res = []
        index = 0
        for key_head in key:
            if self._data[index]:
                res.extend(self._data[index])
            
            if key_head not in self._code_map:
                break 
            code = self._code_map[key_head]

            child = self._find_child(index, code)
            if child < 0:
                break
            index = child
        
        return res

    def _insert(self, index, key, value):
        cur_index = index
        for key_head in key:
            if key_head not in self._code_map:
                self._code_map[key_head] = self._next_code
                self._next_code += 1

            code = self._code_map[key_head]
            if self._base[cur_index] < 0:
                base = self._find_avail_base([code])
                self._set_base(cur_index, base)
            else:
                if self._is_conflicted(cur_index, code):
                    self._modify(cur_index, code)
            
            if code not in self._codes[cur_index]:
                self._codes[cur_index].append(code)
                self._codes[cur_index].sort()
            child = self._base[cur_index] + code
            self._set_check(child, cur_index)
            cur_index = child
           
        if value not in self._data[cur_index]:
            self._data[cur_index].append(value)
        
    def _is_conflicted(self, index, code):
        if self._size <= self._base[index] + code:
            return False
        return self._check[self._base[index] + code] >= 0
    
    def _modify(self, index, new_code):
        codes = self._get_stored_codes(index)
        base = self._find_avail_base(codes + [new_code])
        old_base = self._base[index]
        self._set_base(index, base)
        for code in reversed(codes):
            child_index = self._base[index] + code
            self._set_check(child_index, index)
            old_child_index = old_base + code
            old_child_base = self._base[old_child_index]
            self._set_base(child_index, old_child_base)
            if old_child_base >= 0:
                children_of_old_child = self._get_children(old_child_index)
                for child_of_old_child in children_of_old_child:
                    self._set_check(child_of_old_child, child_index)
            self._codes[child_index] = self._codes[old_child_index]
            self._data[child_index] = self._data[old_child_index]
            
            self._set_base(old_child_index, -1)
            self._set_check(old_child_index, -1)
            self._codes[old_child_index] = []
            self._data[old_child_index] = []

    def _set_base(self, index, base):
        if self._size <= index:
            old_size = self._size
            extend = index - self._size + 1
            self._extend(extend)
            for i in range(self._size - old_size):
                self._check[old_size + i] = -(old_size + i + 1)
            self._check[self._size - 1] = self._empty_node_head
            self._empty_node_head = old_size
            
        self._base[index] = base

    def _set_check(self, index, check):
        if self._size <= index:
            old_size = self._size
            extend = index - self._size + 1
            self._extend(extend)
            self._check[index] = check

            for i in range(extend - 1):
                self._check[old_size + i] = -(old_size + i + 1)
            if extend >= 2:
                self._check[self._size - 2] = -self._size
            else:
                if self._empty_node_head != old_size:
                    old_last_emp_node_index = self._empty_node_head
                    while self._check[old_last_emp_node_index] != -old_size:
                        old_last_emp_node_index = -(self._check[old_last_emp_node_index])
                    self._check[old_last_emp_node_index] = -self._size
                else:
                    self._empty_node_head = self._size
        else:
            if self._check[index] < 0:
                if index == self._empty_node_head:
                    self._empty_node_head = -(self._check[index])
                    self._check[index] = check
                else:
                    emp_node_index = self._empty_node_head
                    while -(self._check[emp_node_index]) != index:
                        emp_node_index = -(self._check[emp_node_index])
                    self._check[emp_node_index] = self._check[index]
                    self._check[index] = check
            elif check < 0:
                if index < self._empty_node_head:
                    self._check[index] = -(self._empty_node_head)
                    self._empty_node_head = index
                else:
                    emp_node_index = self._empty_node_head
                    while not (emp_node_index < index) or not (index < -(self._check[emp_node_index])):
                        emp_node_index = -(self._check[emp_node_index])
                    self._check[index] = self._check[emp_node_index]
                    self._check[emp_node_index] = -index
            else:
                self._check[index] = check

    def _get_stored_codes(self, index):
        return self._codes[index]
        #codes = []
        #for child_index, check in enumerate(self._check):
        #    if check == index:
        #        code = child_index - self._base[index]
        #        if code >= self._next_code:
        #            raise Exception('invalid code: ' + str(code))
        #        codes.append(child_index - self._base[index])

        #return codes

    def _get_children(self, index):
        return map(lambda c: self._base[index] + c, self._codes[index]) 
        #children = []
        #for child_index, check in enumerate(self._check):
        #    if check == index:
        #        children.append(child_index)
        #return children
    
    def _find_avail_base(self, codes):
        def _test_base(self, base, codes):
            for code in codes:
                if (base + code) >= self._size or self._check[base + code] >= 0:
                    return False
            return True
        
        codes.sort()
        min_code = codes[0]
        emp_node_index = self._empty_node_head
        base = emp_node_index - min_code
        while base < 0 or not _test_base(self, base, codes):
            if emp_node_index >= self._size:
                return base 
            emp_node_index = -(self._check[emp_node_index])
            base = emp_node_index - min_code

        return base 

    def _extend(self, extend):
        self._base.extend([-1] * extend)
        self._check.extend([-1] * extend)
        for i in range(extend):
            self._codes.append([])
            self._data.append([])
        self._size += extend
        print('size: ' + str(self._size))
    
    def _search(self, key):
        index = 0
        for pos, key_head in enumerate(key):
            if key_head not in self._code_map:
                return False, index, pos
            code = self._code_map[key_head]
            
            child = self._find_child(index, code)
            if child < 0:
                return False, index, pos
            index = child

        return True, index, -1

    def _find_child(self, parent, code):
        if self._base[parent] < 0:
            return -1
        child = self._base[parent] + code
        if self._size <= child:
            return -1
        return child if self._check[child] == parent else -1
