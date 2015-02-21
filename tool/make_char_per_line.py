# -*- coding: utf-8 -*-

import sys
import glob
import codecs
import os
import datetime
import threading

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

if os.path.exists(out_dir) == False:
    os.mkdir(out_dir)

file_count = 0
for dir_path, sub_dirs, file_names in os.walk(baseDir):
    file_list = glob.glob(os.path.expanduser(dir_path) + '/' + pattern)
    for file in file_list:
        if os.path.isdir(file):
            continue
        print('analyzing ' + file)
        file_count += 1
        out_file = out_dir + '/' + prefix + str(file_count).zfill(4) + '.delim'
        f = codecs.open(file, 'r', 'utf_8')
        with open(out_file, 'w') as outf:
            text = f.read()
            for c in text:
                if c != '\n':
                    outf.write((c + '\n').encode('utf_8'))
        f.close()
