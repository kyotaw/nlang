# -*- coding: utf-8 -*-

import glob
import codecs
import os

class ChasenWord:
	TagTable = {
		u'連体詞':u'T',
		u'接頭詞':u'P',
		u'形容詞接続':u'ADJC',
		u'数接続':u'NUC',
		u'動詞接続':u'VC',
		u'名詞接続':u'NC',
		u'名詞':u'N',
		u'引用文字列':u'QS',
		u'サ変接続':u'SAC',
		u'ナイ形容詞語幹':u'NAI',
		u'形容動詞語幹':u'NAADJSTEM',
		u'動詞非自立的':u'VNI',
		u'副詞可能':u'ADVP',
		u'一般':u'GEN',
		u'数':u'NU',
		u'接続詞的':u'CONJL',
		u'固有名詞':u'PROPN',
		u'人名':u'PERN',
		u'姓':u'FAMN',
		u'名':u'FSTN',
		u'組織':u'ORN',
		u'地域':u'ARN',
		u'国':u'CON',
		u'接尾':u'SF',
		u'助数詞':u'CSUF',
		u'助動詞語幹':u'AUVSTEM',
		u'特殊':u'SP',
		u'代名詞':u'PRON',
		u'縮約':u'CTRA',
		u'非自立':u'NI',
		u'動詞':u'V',
		u'自立':u'I',
		u'形容詞':u'ADJ',
		u'副詞':u'ADV',
		u'助詞類接続':u'ADVC',
		u'接続詞':u'CONJ',
		u'助詞':u'J',
		u'格助詞':u'JK',
		u'引用':u'Q',
		u'連語':u'COL',
		u'係助詞':u'JB',
		u'終助詞':u'JS',
		u'接続助詞':u'JCONJ',
		u'副詞化':u'ADVL',
		u'副助詞':u'JF',
		u'並立助詞':u'JH',
		u'連体化':u'TL',
		u'副助詞／並立助詞／終助詞':u'JF/JH/JS',
		u'助動詞':u'AUV',
		u'感動詞':u'IM',
		u'記号':u'SY',
		u'句点':u'PE',
		u'読点':u'COM',
		u'空白':u'SPC',
		u'アルファベット':u'AL',
		u'括弧開':u'BRA',
		u'括弧閉':u'KET',
		u'フィラー':u'FIL',
		u'その他':u'OT',
		u'間投':u'IN',
		u'未知語':u'UNK',

		u'未然形':u'Z',
		u'連用形':u'Y',
		u'終止形':u'S',
		u'基本形':u'S',
		u'連体形':u'T',
		u'命令形':u'R'
	}

	def __init__(self, raw):
		self.valid = False
		self.raw = raw
		tokens = raw[:-1].split('\t')
		if (len(tokens) < 4):
			return
		
		self.appear = tokens[0]
		self.pron = tokens[1]
		self.base = tokens[2]
		parts = tokens[3].split('-')
		self.parts = (p for p in parts)
		if (len(tokens) > 4):
			self.conj_form = tokens[4]
		else:
			self.conj_form = ''
			self.conj_type = ''
		if (len(tokens) > 5):
			self.conj_type = tokens[5]
		else:
			self.conj_type = ''

		self.valid = True

	def tag(self):
		tag = ''
		for p in self.parts:
			if tag:
				tag = tag + '-'
			tag = tag + ChasenWord.TagTable[p]
		if self.conj_type and self.conj_type in ChasenWord.TagTable:
			tag += '-' + ChasenWord.TagTable[self.conj_type]
		return tag

class ChasenCorpusReader:
	def __init__(self, path, file_pattern, encoding):
		if file_pattern == '':
			self.file_list = glob.glob(os.path.expanduser(path))
		else:
			self.file_list = glob.glob(os.path.expanduser(path) + '/' + file_pattern)
		self.encoding = encoding
		self.vocabulary = []
		for file in self.file_list:
			self.__read(file, encoding)

	def words(self):
		return [w.appear for w in self.vocabulary]

	def tagged_words(self):
		return [(w.appear, w.pron, w.tag()) for w in self.vocabulary]

	def __read(self, file_path, encoding):
		f = codecs.open(file_path, 'r', encoding)
		for line in f.readlines():
			w = ChasenWord(line)
			if (w.valid):
				self.vocabulary.append(w)
