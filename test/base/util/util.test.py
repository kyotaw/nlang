# -*- coding: utf-8 -*-

from nlang.base.util.util import *

all_pass = True

def test(c, t, ans):
	if t != ans:
		print(pp(c) + ' is not ' + ans + ' but ' + t)
		return False
	return True

ans = 'ascii'
c = u'a'
t = get_char_type(c)
all_pass &= test(c, t, ans)

ans = 'alpha_zenkaku'
c = u'A'
t = get_char_type(c)
all_pass &= test(c, t, ans)

ans = 'hiragana'
c = u'あ'
t = get_char_type(c)
all_pass &= test(c, t, ans)

ans = 'katakana_zenkaku'
c = u'ア'
t = get_char_type(c)
all_pass &= test(c, t, ans)

ans = 'katakana_hankaku'
c = u'ｱ'
t = get_char_type(c)
all_pass &= test(c, t, ans)

ans = 'kanji'
c = u'水'
t = get_char_type(c)
all_pass &= test(c, t, ans)

ans = 'unknown'
c = u''
t = get_char_type(c)
all_pass &= test(c, t, ans)

if all_pass:
	print('all passed!')
	
