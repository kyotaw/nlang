# -*- coding: utf-8 -*-

import glob
import codecs
import os

class BaseReader(object):
	def __init__(self, path='', file_pattern='', encoding='utf-8'):
		self.vocabulary = []
		if path:
			if file_pattern == '':
				self.file_list = glob.glob(os.path.expanduser(path))
			else:
				self.file_list = glob.glob(os.path.expanduser(path) + '/' + file_pattern)
			for file in self.file_list:
				self.read(file, encoding)

	def words(self):
		return [w.lemma for w in self.vocabulary]

