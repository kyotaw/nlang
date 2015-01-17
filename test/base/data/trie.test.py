# -*- coding: utf-8 -*-

from nlang.base.data.trie import Trie
import pprint

trie = Trie()

all_path = True

#count function test

test_item = 'test1'
test_key = 'test1'
test_value = 'blue'

#エントリなし
if trie.count(test_key, test_value) != 0:
	print('-Failed: ' + test_item + ' key: ' + test_key + ' value: ' + test_value)
	all_path = False

#1エントリ
test_item = 'test2'
trie.insert(test_key, test_value)
count = trie.count(test_key, test_value)
if count != 1:
	print('-Failed: ' + test_item + ' key: ' + test_key + ' value: ' + test_value)
	all_path = False

#2エントリ
test_item = 'test3'
trie.insert(test_key, test_value)
if trie.count(test_key, test_value) != 2:
	print('-Failed: ' + test_item + ' key: ' + test_key + ' value: ' + test_value)
	all_path = False

#存在しない値
test_item = 'test4'
if trie.count(test_key, 'value') != 0:
	print('-Failed: ' + test_item + ' key: ' + test_key + ' value: ' + test_value)
	all_path = False

#存在しないキー
test_item = 'test5'
if trie.count('key', test_value) != 0:
	print('-Failed: ' + test_item + ' key: ' + test_key + ' value: ' + test_value)
	all_path = False



if all_path:
	print('All Passed !!')
