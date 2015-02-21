# -*- coding: utf-8 -*-

import sys
import glob
import os
import datetime
import argparse

from nlang.corpus.chasen.chasen_reader import ChasenCorpusReader
from nlang.corpus.jugo.jugo_reader import JugoCorpusReader
from nlang.analyzer.connectivity_analyzer import ConnectivityAnalyzer
from nlang.base.data.cost_calculator import calculate_cost


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--src_root_path', nargs=None, type=str, action='store')
    parser.add_argument('-f', '--file_pattern', nargs=None, type=str, action='store')
    parser.add_argument('-o', '--out_filename', nargs='?', default='out', type=str, action='store')
    args = parser.parse_args()

    start = datetime.datetime.now()

    analyzer = ConnectivityAnalyzer()
    for dir_path, sub_dirs, file_names in os.walk(args.src_root_path):
        file_list = glob.glob(os.path.expanduser(dir_path) + '/' + args.file_pattern)
        for file in file_list:
            root, ext = os.path.splitext(file)
            r = None
            if ext == ".chasen":
                r = ChasenCorpusReader(file)
            elif ext == ".jugo":
                r = JugoCorpusReader(file)
            if r:
                print('analyzing ' + file)
                analyzer.analyze(r.tagged_words())

    print('writing connectivity table...')

    with open('.'.join([args.out_filename, 'conn']), 'w') as f:
        for tag, connects in analyzer.connect_table.items():
            line = tag
            for i, val in enumerate(connects):
                line += '\t' + val + ':' + str(calculate_cost(analyzer.probability(tag, val)))
            line += '\n'
            f.write(line)

    time = datetime.datetime.now() - start
    print('completed! time : ' + str(time.seconds) + ' sec')
