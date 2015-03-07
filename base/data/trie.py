# -*- coding: utf-8 -*-


class Trie(object):
    def __init__(self):
        self._root = {}

    def insert(self, key, value):
        node = self._root
        for key_head in key:
            if key_head not in node:
                node[key_head] = {}
            node = node[key_head]
        
        if 'value' not in node:
            node['value'] = []
        for pkg in node['value']:
            if value == pkg['data']:
                pkg['count'] += 1
                return
        node['value'].append({'data': value, 'count': 1})
    
    def common_prefix_search(self, key):
        data = []
        node = self._root
        for key_head in key:
            if 'value' in node:
                for pkg in node['value']:
                    data.append(pkg['data'])
            if key_head not in node:
                break
            node = node[key_head]
        if 'value' in node:
            for pkg in node['value']:
                data.append(pkg['data'])
        return data
    
    def get(self, key):
        value_list = self._search(key)
        if value_list is None:
            return None
        return [pkg['data'] for pkg in value_list]
    
    def count(self, key, value):
        value_list = self._search(key)
        if value_list is None:
            return 0
        
        for pkg in value_list:
            if value == pkg['data']:
                return pkg['count']
        return 0
        
    def dump(self):
        return self._dump(self._root, [])
    
    def _search(self, key):
        node = self._root
        for key_head in key:
            if key_head not in node:
                return None
            node = node[key_head]
            
        if 'value' not in node:
            return None
        return node['value']

    def _dump(self, node, key):
        data = []
        if 'value' in node:
            k = key[:]
            for pkg in node['value']:
                data.append((k, pkg['data']))

        for label, child_node in node.items():
            if label != 'value':
                child_key = key[:]
                child_key.append(label)
                data += self._dump(child_node, child_key)
        
        return data
