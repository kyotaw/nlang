# -*- coding: utf-8 -*-


class Trie(object):
    def __init__(self):
        self.root = {}

    def insert(self, key, value):
        self._insert(self.root, key, value)

    def common_prefix_search(self, key):
        return self._common_prefix_search(self.root, key)

    def get(self, key):
        return self._get(self.root, key)

    def count(self, key, value):
        return self._count(self.root, key, value)

    def dump(self):
        data = []
        self._dump(self.root, [], data)
        return data

    def _insert(self, dict, key, value):
        if key:
            key_head = key[0]
            if key_head not in dict:
                dict[key_head] = {}
            self._insert(dict[key_head], key[1:], value)
        else:
            if 'value' not in dict:
                dict['value'] = []
            for pkg in dict['value']:
                if value == pkg['data']:
                    pkg['count'] += 1
                    return
            dict['value'].append({'data': value, 'count': 1})

    def _common_prefix_search(self, dict, key):
        data = []
        if 'value' in dict:
            for pkg in dict['value']:
                data.append(pkg['data'])
        if key:
            key_head = key[0]
            if key_head in dict:
                data += self._common_prefix_search(dict[key_head], key[1:])
        return data

    def _get(self, dict, key):
        if key:
            key_head = key[0]
            if key_head not in dict:
                return []
            return self._get(dict[key_head], key[1:])
        else:
            if 'value' not in dict:
                return []
            return [pkg['data'] for pkg in dict['value']]

    def _count(self, dict, key, value):
        if key:
            key_head = key[0]
            if key_head not in dict:
                return 0
            return self._count(dict[key_head], key[1:], value)
        else:
            if 'value' not in dict:
                return 0
            for pkg in dict['value']:
                if value == pkg['data']:
                    return pkg['count']
            return 0

    def _dump(self, dict, key, data):
        if 'value' in dict:
            k = key[:]
            for pkg in dict['value']:
                data.append((k, pkg['data']))

        for k, v in dict.items():
            if k != 'value':
                child_key = key[:]
                child_key.append(k)
                self._dump(v, child_key, data)
