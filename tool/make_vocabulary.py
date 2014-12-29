# -*- coding: utf-8 -*-

from nlang.corpus.chasen.chasen_reader import ChasenCorpusReader
from nlang.base.data.trie import Trie
from nlang.analyzer.vocabulary_analyzer import VocabularyAnalyzer
from nlang.tool.cost_calculator import calculate_cost
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

def analyze_func(analyzer, words):
	analyzer.analyze(words)

def vocab_func(vocab, words):
	for word in words:
		if word['pron']:
			vocab.insert(word['pron'], word)

start = datetime.datetime.now()

vocab = Trie()
analyzer = VocabularyAnalyzer()
for dir_path, sub_dirs, file_names in os.walk(baseDir):
	file_list = glob.glob(os.path.expanduser(dir_path) + '/' + pattern)
	for file in file_list:
		print('analyzing ' + file)
		r = ChasenCorpusReader(file, '', 'utf-8')
		words = r.tagged_words()
		for word in words:
			if word['pron']:
				vocab.insert(word['pron'], word)
		analyzer.analyze(words)
#		analyze_thread = threading.Thread(target=analyze_func, args=(analyzer, words))
#		analyze_thread.start()
#		vocab_thread = threading.Thread(target=vocab_func, args=(vocab, words))
#		vocab_thread.start()
#		analyze_thread.join()
#		vocab_thread.join()

with open(out_file, 'wb') as f:
	for tagged_word in vocab.dump():
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

