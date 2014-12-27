# -*- coding: utf-8 -*-

from nlang.corpus.reader.chasen import *
from nlang.base.data.trie import *
from nlang.corpus.analyzer.vocabulary_analyzer import VocabularyAnalyzer
from nlang.tool.cost_calculator import calculate_cost
import re, pprint
import sys
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
	for word in tagged:
		if word[1]:
			vocab.insert(word[1], word)

start = datetime.datetime.now()

vocab = Trie()
analyzer = VocabularyAnalyzer()
for dir_path, sub_dirs, file_names in os.walk(baseDir):
	file_list = glob.glob(os.path.expanduser(dir_path) + '/' + pattern)
	for file in file_list:
		print('analyzing ' + file)
		r = ChasenCorpusReader(file, '', 'utf-8')
		tagged = r.tagged_words()
		analyze_thread = threading.Thread(target=analyze_func, args=(analyzer, tagged))
		analyze_thread.start()
		vocab_thread = threading.Thread(target=vocab_func, args=(vocab, tagged))
		vocab_thread.start()
		analyze_thread.join()
		vocab_thread.join()

with open(out_file, 'wb') as f:
	for tagged_word in vocab.dump():
		line = u''
		line += tagged_word[0] + u'\t' #lemmma
		line += tagged_word[1] + u'\t' #pron
		line += tagged_word[2] + u'\t' #pos
		line += str(calculate_cost(analyzer.probability(tagged_word[0], tagged_word[2]))) #probability
		line += u'\n'
		f.write(line.encode('utf-8'))

time = datetime.datetime.now() - start
print('completed! time : ' + str(time.seconds) + ' sec')

