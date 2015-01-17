# -*- coding: utf-8 -*-

import sys
import pickle
import os
import glob
from nlang.processor.tokenizer import Tokenizer

if len(sys.argv) < 3:
	print('usage chunker_trainer.py baseDir fileNamePattern train_count')
	quit()

baseDir = sys.argv[1]
pattern = sys.argv[2]
count = 100
if len(sys.argv) > 3:
    count = sys.argv[3]

tokenizer = Tokenizer()
with open('tokenizer.pickle', 'wb') as f:
    pickle.dump(tokenizer, f)


