# -*- coding: utf-8 -*-
def code_point(c):
	return ord(c) if len(c) > 0 else -1

def is_ascii(c):
	cp = code_point(c)
	return True if 0x0000 <= cp and cp <= 0x007F else False

def is_alpha_zenkaku(c):
	cp = code_point(c)
	return True if 0xFF01 <= cp and cp <= 0xFF5D else False	

def is_hiragana(c):
	cp = code_point(c)
	return True if 0x3040 <= cp and cp <= 0x309F else False

def is_katakana_zenkaku(c):
	cp = code_point(c)
	return True if 0x30A0 <= cp and cp <= 0x30FF else False

def is_katakana_hankaku(c):
	cp = code_point(c)
	return True if 0xFF61 <= cp and cp <= 0xFF9F else False

def is_kanji(c):
	cp = code_point(c)
	return True if 0x4E00 <= cp and cp <= 0x9FCF else False

