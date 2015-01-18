# -*- coding: utf-8 -*-

from nlang.corpus.chasen.chasen_reader import ChasenCorpusReader
from nlang.corpus.jugo.jugo_reader import JugoCorpusReader
from nlang.analyzer.connectivity_analyzer import ConnectivityAnalyzer
from nlang.base.data.cost_calculator import calculate_cost
import re, pprint
import sys
import glob
import codecs
import os
import datetime
import threading

if len(sys.argv) < 3:
	print('usage make_connectability_table.py baseDir fileNamePattern outFileName')
	quit()

baseDir = sys.argv[1]
pattern = sys.argv[2]
out_file = 'out'
if len(sys.argv) > 3:
	out_file = sys.argv[3]
out_file += '.conn'

start = datetime.datetime.now()

analyzer = ConnectivityAnalyzer()
for dir_path, sub_dirs, file_names in os.walk(baseDir):
	file_list = glob.glob(os.path.expanduser(dir_path) + '/' + pattern)
	for file in file_list:
		print('analyzing ' + file)
                root, ext = os.path.splitext(file)
                r = None
                if ext == ".chasen":
		    r = ChasenCorpusReader(file, '', 'utf-8')
                elif ext == ".jugo":
                    r = JugoCorpusReader(file, '', 'utf-8')
                if r:
                    analyzer.analyze(r.tagged_words())

print('writing connectivity table...')

with open(out_file, 'wb') as f:
	for pos, connects in analyzer.connect_table.items():
		row = pos
		for i, val in enumerate(connects):
			row += '\t' + val + ':' + str(calculate_cost(analyzer.probability(pos, val)))
		row += '\n'
		f.write(row.encode('utf-8'))

time = datetime.datetime.now() - start
print('completed! time : ' + str(time.seconds) + ' sec')

