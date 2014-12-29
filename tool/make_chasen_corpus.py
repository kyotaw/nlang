# -*- coding: utf-8 -*-

import re, pprint
import sys
import glob
import codecs
import os
import datetime
import threading

from nlang.processor.separator import Separator

if len(sys.argv) < 3:
	print('usage make_chasen_corpus.py baseDir fileNamePattern outFileName')
	quit()

baseDir = sys.argv[1]
pattern = sys.argv[2]
out_file = 'out'
if len(sys.argv) > 3:
	out_file = sys.argv[3]
out_file += '.chasen'

start = datetime.datetime.now()

separator = Separator()
for dir_path, sub_dirs, file_names in os.walk(baseDir):
	file_list = glob.glob(os.path.expanduser(dir_path) + '/' + pattern)
	for file in file_list:
		print('analyzing ' + file)

		with open(file, 'r') as f:
