# -*- coding: utf-8 -*-

import re, pprint
import sys
import glob
import codecs
import os
import datetime
import threading
from nlang.corpus.jugo.jugo_reader import JugoCorpusReader
from nlang.analyzer.phrase_analyzer import PhraseAnalyzer
from nlang.base.data.cost_calculator import calculate_cost
from nlang.base.data.trie import Trie

if len(sys.argv) < 3:
	print('usage make_phrase_pattern.py baseDir fileNamePattern outFileName')
	quit()

baseDir = sys.argv[1]
pattern = sys.argv[2]
out_file = 'out'
if len(sys.argv) > 3:
	out_file = sys.argv[3]

start = datetime.datetime.now()

analyzer = PhraseAnalyzer()
for dir_path, sub_dirs, file_names in os.walk(baseDir):
	file_list = glob.glob(os.path.expanduser(dir_path) + '/' + pattern)
	for file in file_list:
		print('analyzing ' + file)
		r = JugoCorpusReader(file, '', 'utf-8')
		analyzer.analyze(r.tagged_words())

with open(out_file + '.phrase', 'wb') as f:
	for phrase in analyzer.calc_phrase_probability():
		line = u''
		line += phrase[0] + '\t'
		line += phrase[1] + '\t'
		line += str(calculate_cost(phrase[2])) + '\n'
		f.write(line.encode('utf-8'))

with open(out_file + '.iob_conn', 'wb') as f:
	for left_pos, right_pos_list in analyzer.calc_enter_conn_probability().items():
		line = u''
		line += left_pos 
		for right_pos in right_pos_list:
			line += '\t' + right_pos[0] + ':' + str(calculate_cost(right_pos[1]))
		line += '\n'
		f.write(line.encode('utf-8'))

time = datetime.datetime.now() - start
print('completed! time : ' + str(time.seconds) + ' sec')
