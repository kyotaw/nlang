# -*- coding: utf-8 -*-

import re, pprint
import sys
import glob
import codecs
import os
import datetime
import threading

from nlang.processor.tokenizer import Tokenizer
from nlang.corpus.chasen.chasen_writer import ChasenCorpusWriter
from nlang.base.util.util import *

if len(sys.argv) < 3:
	print('usage make_chasen_corpus.py baseDir fileNamePattern outDir filePrefix')
	quit()

baseDir = sys.argv[1]
pattern = sys.argv[2]
out_dir = 'out'
if len(sys.argv) > 3 and sys.argv[3] != '':
	out_dir = sys.argv[3]
prefix = ''
if len(sys.argv) > 4 and sys.argv[4] != '':
	prefix = sys.argv[4]

start = datetime.datetime.now()

if os.path.exists(out_dir) == False:
	os.mkdir(out_dir)

separator = Tokenizer()

file_count = 0
for dir_path, sub_dirs, file_names in os.walk(baseDir):
	file_list = glob.glob(os.path.expanduser(dir_path) + '/' + pattern)
	for file in file_list:
            if os.path.isdir(file):
                continue

	    print('analyzing ' + file)
	    file_count += 1
	    out_file = out_dir + '/' + prefix + str(file_count).zfill(4) + '.chasen'	
	    with open(file, 'r') as f:
		tagged_words = separator.tag((f.read().decode('utf-8')))
		ChasenCorpusWriter(out_file, tagged_words)

time = datetime.datetime.now() - start
print('completed! time : ' + str(time.seconds) + ' sec')
