# -*- coding: utf-8 -*-

import sys
import pickle
import os
import glob
import argparse
import codecs

from nlang.base.system import env
from nlang.base.util.util import pp
from nlang.processor.sentencer import Sentencer, SentencerImpl

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--src_root_path', nargs=None, type=str, action='store')
    parser.add_argument('-f', '--file_pattern', nargs=None, type=str, action='store')
    args = parser.parse_args()

    sentencer = Sentencer(True)
    for dir_path, sub_dirs, file_names in os.walk(args.src_root_path):
        file_list = glob.glob(os.path.expanduser(dir_path) + '/' + args.file_pattern)
        for file in file_list:
            if os.path.isdir(file):
                continue
            f = codecs.open(file, 'r', 'utf_8')
            cur_line = f.readline()
            if not cur_line:
                continue

            print('training sentencer by ' + file)

            tokens = cur_line[:-1].split('\t')
            prev_char = ''
            cur_char = tokens[0]
            cur_delim = True if len(tokens) > 1 and tokens[1] == 'D' else False
            next_char = ''
            next_line = f.readline()
            while next_line:
                tokens = next_line[:-1].split('\t')
                next_char = tokens[0]
                next_delim = True if len(tokens) > 1 and tokens[1] == 'D' else False
                sentencer.train((cur_delim, SentencerImpl.get_feature(cur_char, prev_char, next_char)))
                prev_char = cur_char
                cur_char = next_char
                cur_delim = next_delim
                next_char = ''
                next_line = f.readline()

            sentencer.train((cur_delim, SentencerImpl.get_feature(cur_char, prev_char, next_char)))
            f.close()

    with open('sentencer.pickle', 'wb') as f:
        pickle.dump(sentencer, f)
