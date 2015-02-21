# -*- coding: utf-8 -*-

import sys
import glob
import os
import datetime
import argparse

from nlang.corpus.chasen.chasen_reader import ChasenCorpusReader
from nlang.corpus.jugo.jugo_reader import JugoCorpusReader
from nlang.base.data.trie import Trie
from nlang.analyzer.vocabulary_analyzer import VocabularyAnalyzer
from nlang.base.data.cost_calculator import calculate_cost

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--src_root_path', nargs=None, type=str, action='store')
    parser.add_argument('-f', '--file_pattern', nargs=None, type=str, action='store')
    parser.add_argument('-o', '--out_filename', nargs='?', default='out', type=str, action='store')
    args = parser.parse_args()

    start = datetime.datetime.now()

    vocab = Trie()
    analyzer = VocabularyAnalyzer()
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
                words = r.tagged_words()
                for word in words:
                    if word.pron:
                        vocab.insert(word.pron, word)
                analyzer.analyze(words)

    with open('.'.join([args.out_filename, 'vocab']), 'w') as f:
        for key_val in vocab.dump():
            word = key_val[1]
            if word.pos[0] == 'UNK':
                continue
            line = '\t'.join([word.lemma, word.pron, word.base, '-'.join(word.pos)])
            if word.conj_type:
                line = '\t'.join([line, word.conj_type])
            if word.conj_form:
                line = '\t'.join([line, word.conj_form])
            line = '\t'.join([line, str(calculate_cost(analyzer.probability(word.lemma, word.tag)))])
            line += '\n'
            f.write(line)

    time = datetime.datetime.now() - start
    print('completed! time : ' + str(time.seconds) + ' sec')
