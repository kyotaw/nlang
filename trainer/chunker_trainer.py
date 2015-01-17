# -*- coding: utf-8 -*-

import sys
import pickle
import os
import glob
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
            jugo_words = reader.tagged_words()
            tagged_words = [w[1] for w in jugo_words]
            for i in range(int(count)):
                if chunker.train(tagged_words, jugo_words):
                    print('passed: ' + file)
                    break

with open('chuncker.pickle', 'wb') as f:
    pickle.dump(chunker, f)


