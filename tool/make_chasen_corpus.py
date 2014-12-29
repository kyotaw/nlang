# -*- coding: utf-8 -*-

import re, pprint
import sys
import glob
import codecs
import os
import datetime
import threading

from nlang.processor.separator import Separator
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

separator = Separator()
for dir_path, sub_dirs, file_names in os.walk(baseDir):
	file_list = glob.glob(os.path.expanduser(dir_path) + '/' + pattern)
	for file in file_list:
		print('analyzing ' + file)
		out_file = out_dir + '/' + prefix + os.path.basename(file) + '.chasen'	
		with open(file, 'r') as f:
			tagged_words = separator.tagg((f.read().decode('utf-8')))
			ChasenCorpusWriter(out_file, tagged_words)
