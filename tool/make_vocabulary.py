# -*- coding: utf-8 -*-

from nlang.corpus.chasen.chasen_reader import ChasenCorpusReader
from nlang.corpus.jugo.jugo_reader import JugoCorpusReader
from nlang.base.data.trie import Trie
from nlang.analyzer.vocabulary_analyzer import VocabularyAnalyzer
from nlang.base.data.cost_calculator import calculate_cost
import re, pprint
import sys
import glob
import codecs
import os
import datetime
import threading

if len(sys.argv) < 3:
	print('usage make_vovabulary_table.py baseDir fileNamePattern outFileName')
	quit()

baseDir = sys.argv[1]
pattern = sys.argv[2]
out_file = 'out'
if len(sys.argv) > 3:
	out_file = sys.argv[3]
out_file += '.vocab'

start = datetime.datetime.now()

vocab = Trie()
analyzer = VocabularyAnalyzer()
for dir_path, sub_dirs, file_names in os.walk(baseDir):
	file_list = glob.glob(os.path.expanduser(dir_path) + '/' + pattern)
	for file in file_list:
		print('analyzing ' + file)
                root, ext = os.path.splitext(file)
                r = None
                if ext == ".chasen":
		    r = ChasenCorpusReader(file, '', 'utf-8')
                elif ext == ".jugo":
                    r = JugoCorpusReader(file, '', 'utf-8')
                if r:
                    words = r.tagged_words()
		    for word in words:
		    	if word['pron']:
		    	    vocab.insert(word['pron'], word)
		    analyzer.analyze(words)

with open(out_file, 'wb') as f:
	for key_val in vocab.dump():
		tagged_word = key_val[1]
		line = u''
		line += tagged_word['lemma'] + u'\t'
		line += tagged_word['pron'] + u'\t'
		line += tagged_word['base'] + u'\t'
		line += tagged_word['pos'] + u'\t'
		if tagged_word['conj_form']:
			line += tagged_word['conj_form'] + u'\t'
		if tagged_word['conj_type']:
			line += tagged_word['conj_type'] + u'\t'
		line += str(calculate_cost(analyzer.probability(tagged_word['lemma'], tagged_word['pos']))) #probability
		line += u'\n'
		f.write(line.encode('utf-8'))

time = datetime.datetime.now() - start
print('completed! time : ' + str(time.seconds) + ' sec')

