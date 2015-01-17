# -*- coding: utf-8 -*- 

from nlang.base.util.util import pp
from nlang.processor.tokenizer import Tokenizer

s = Tokenizer()
r = s.tag(u'東京　２７日　ロイター］- 政府は２７日、景気の下支えに向けた３．５兆円の経済対策を閣議決定した。地方自治体の状況に応じて柔軟に活用できる交付金を創設するなどし、国内総生産（ＧＤＰ、実質）を０．７％程度増やす狙い。来春の統一地方選をにらみ、地域経済を下支えする姿を鮮明にする。')

rr = []
for l in r:
	rr.append((l['lemma'], l['pos']))
print pp(rr)
