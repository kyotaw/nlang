# -*- coding: utf-8 -*-

import sys
import glob
import os
import datetime
import argparse

from nlang.corpus.chasen.chasen_reader import ChasenCorpusReader
from nlang.corpus.jugo.jugo_reader import JugoCorpusReader
from nlang.base.data.trie import Trie
from nlang.base.util.unicode_util import unicode_range, code_point
from nlang.analyzer.vocabulary_analyzer import VocabularyAnalyzer
from nlang.base.data.cost_calculator import calculate_cost


def get_range(c):
    cp = code_point(c)
    for r in unicode_range:
        if r[0] <= cp and cp <= r[1]:
            return r 
    raise Exception(c + 'is unicode out of range')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--src_root_path', nargs=None, type=str, action='store')
    parser.add_argument('-f', '--file_pattern', nargs=None, type=str, action='store')
    parser.add_argument('-o', '--out_foldername', nargs='?', default='out', type=str, action='store')
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
                        vocab.insert(word.lemma, word)
                analyzer.analyze(words)

    if not os.path.exists(args.out_foldername):
        os.mkdir(args.out_foldername)
   
    files = {}
    for uni_range in unicode_range:
        files[uni_range] = open(args.out_foldername + '/' + '_'.join(map(lambda x: hex(x), uni_range)), 'w')
    
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
        
        uni_range = get_range(word.lemma[0])
        files[uni_range].write(line)
    
    for f in files.values():
        f.close()

    time = datetime.datetime.now() - start
    print('completed! time : ' + str(time.seconds) + ' sec')
