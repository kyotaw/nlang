# -*- coding: utf-8 -*-

import sys
import glob
import os
import datetime
import argparse

from nlang.corpus.jugo.jugo_reader import JugoCorpusReader
from nlang.analyzer.clause_analyzer import ClauseAnalyzer
from nlang.base.data.cost_calculator import calculate_cost
from nlang.base.data.trie import Trie

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--src_root_path', nargs=None, type=str, action='store')
    parser.add_argument('-f', '--file_pattern', nargs=None, type=str, action='store')
    parser.add_argument('-o', '--out_filename', nargs='?', default='out', type=str, action='store')
    args = parser.parse_args()

    start = datetime.datetime.now()

    analyzer = ClauseAnalyzer()
    for dir_path, sub_dirs, file_names in os.walk(args.src_root_path):
        file_list = glob.glob(os.path.expanduser(dir_path) + '/' + args.file_pattern)
        for file in file_list:
            if os.path.isdir(file):
                continue
            print('analyzing ' + file)
            r = JugoCorpusReader(file)
            analyzer.analyze(r.claused_words())

    with open(args.out_filename + '.clause', 'w') as f:
        for clause in analyzer.calc_clause_probability():
            line = '\t'.join([clause[0], clause[1], str(calculate_cost(clause[2]))])
            line += '\n'
            f.write(line)

    with open(args.out_filename + '.iob_conn', 'w') as f:
        for left_pos, right_pos_list in analyzer.calc_enter_conn_probability().items():
            line = left_pos
            for right_pos in right_pos_list:
                line += '\t' + right_pos[0] + ':' + str(calculate_cost(right_pos[1]))
            line += '\n'
            f.write(line)

    time = datetime.datetime.now() - start
    print('completed! time : ' + str(time.seconds) + ' sec')
