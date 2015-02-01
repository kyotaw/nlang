# -*- coding: utf-8 -*-

import sys
import pickle
import os
import glob
import codecs
import pickle
from nlang.base.system import env
from nlang.base.util.util import pp
from nlang.processor.sentencer import Sentencer, SentencerImpl

if len(sys.argv) < 3:
    print('usage sentencer_trainer.py baseDir fileNamePattern')
    quit()

baseDir = sys.argv[1]
pattern = sys.argv[2]

sentencer = Sentencer()
for dir_path, sub_dirs, file_names in os.walk(baseDir):
    file_list = glob.glob(os.path.expanduser(dir_path) + '/' + pattern)
    for file in file_list:
        if os.path.isdir(file):
            continue
        f = codecs.open(file, 'r', 'utf_8')
        cur_line = f.readline()
        if not cur_line:
            continue
        tokens = cur_line[:-1].split('\t')
        prev_char = u''
        cur_char = tokens[0]
        cur_delim = True if len(tokens) > 1 and tokens[1] == u'D' else False
        next_char = u''
        next_line = f.readline()
        while next_line:
            tokens = next_line[:-1].split('\t')
            next_char = tokens[0]
            next_delim = True if len(tokens) > 1 and tokens[1] == 'D' else False
            sentencer.train((cur_delim, SentencerImpl.get_feature(cur_char, prev_char, next_char)))
            prev_char = cur_char
            cur_char = next_char
            cur_delim = next_delim
            next_char = u''
            next_line = f.readline()

        sentencer.train((cur_delim, SentencerImpl.get_feature(cur_char, prev_char, next_char)))
        f.close()
        
with open('sentencer.pickle', 'wb') as f:
    pickle.dump(sentencer, f)
