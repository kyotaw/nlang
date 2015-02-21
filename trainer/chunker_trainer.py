# -*- coding: utf-8 -*-

import sys
import pickle
import os
import glob
import argparse

from nlang.base.system import env
from nlang.processor.chunker import Chunker
from nlang.corpus.jugo.jugo_reader import JugoCorpusReader


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--src_root_path', nargs=None, type=str, action='store')
    parser.add_argument('-f', '--file_pattern', nargs=None, type=str, action='store')
    parser.add_argument('-c', '--train_count', nargs='?', default='20', type=int, action='store')
    args = parser.parse_args()

    chunker = Chunker(True)
    for dir_path, sub_dirs, file_names in os.walk(args.src_root_path):
        file_list = glob.glob(os.path.expanduser(dir_path) + '/' + args.file_pattern)
        for file in file_list:
            if os.path.isdir(file):
                continue
            reader = JugoCorpusReader(file)
            claused_words = reader.claused_words()
            tagged_words = [w[1] for w in claused_words]

            print('training chunker with : ' + file)

            for i in range(int(args.train_count)):
                if chunker.train(tagged_words, claused_words):
                    print('passed: ' + file)
                    break

    with open('out.clause.trained', 'w') as f:
        for clause in chunker._clauses.dump():
            line = '\t'.join([clause[1][0], clause[1][1], str(clause[1][2])])
            line += '\n'
            f.write(line)

    with open('out.iob_conn.trained', 'w') as f:
        for left_pos, right_pos_list in chunker._iob_conn._table.items():
            line = left_pos
            for right_pos, cost in right_pos_list.items():
                line += '\t' + right_pos + ':' + str(cost)
            line += '\n'
            f.write(line)

    with open('chunker.pickle', 'wb') as f:
        pickle.dump(chunker, f)
