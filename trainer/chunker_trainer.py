# -*- coding: utf-8 -*-

import sys
import pickle
import os
import glob
from nlang.base.system import env
from nlang.processor.chunker import Chunker
from nlang.corpus.jugo.jugo_reader import JugoCorpusReader

if len(sys.argv) < 3:
	print('usage chunker_trainer.py baseDir fileNamePattern train_count')
	quit()

baseDir = sys.argv[1]
pattern = sys.argv[2]
count = 100
if len(sys.argv) > 3:
    count = sys.argv[3]

chunker = Chunker()
for dir_path, sub_dirs, file_names in os.walk(baseDir):
	file_list = glob.glob(os.path.expanduser(dir_path) + '/' + pattern)
	for file in file_list:
            reader = JugoCorpusReader(file)
            jugo_words = reader.claused_words()
            tagged_words = [w[1] for w in jugo_words]
            for i in range(int(count)):
                if chunker.train(tagged_words, jugo_words):
                    print('passed: ' + file)
                    break

with open('out.clause.trained', 'wb') as f:
	for clause in chunker._Chunker__clauses.dump():
		line = u''
		line += clause[1][0] + '\t'
		line += clause[1][1] + '\t'
		line += str(clause[1][2]) + '\n'
		f.write(line.encode('utf-8'))

with open('out.iob_conn.trained', 'wb') as f:
	for left_pos, right_pos_list in chunker._Chunker__iob_conn._ConnectivityTable__table.items():
		line = u''
		line += left_pos 
                for right_pos, cost in right_pos_list.items():
			line += '\t' + right_pos + ':' + str(cost)
		line += '\n'
		f.write(line.encode('utf-8'))

with open('chunker.pickle', 'wb') as f:
    pickle.dump(chunker, f)


