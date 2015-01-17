# -*- coding: utf-8 -*- 

from nlang.base.util.util import pp
from nlang.processor.tokenizer import Tokenizer
from nlang.processor.chunker import Chunker

s = Tokenizer()
#r = s.tag(u'東京　２７日　ロイター］- 政府は２７日、景気の下支えに向けた３．５兆円の経済対策を閣議決定した。地方自治体の状況に応じて柔軟に活用できる交付金を創設するなどし、国内総生産（ＧＤＰ、実質）を０．７％程度増やす狙い。来春の統一地方選をにらみ、地域経済を下支えする姿を鮮明にする。')

r = s.tag(u'温泉街にはつきものの、性に関するテーマパーク的施設「秘宝館」。昭和末期には全国２０館以上あったものの近年は急減、今年１月から日本唯一の存在になったのが「熱海秘宝館」（静岡県熱海市）だ。')
ff = []
for f in r:
	ff.append((f['lemma'], f['pos']))
print pp(ff)
c = Chunker()
rr = c.phrase(r)
#r = s.tag(u'自然災害なんかじゃない。')
#print pp(r)
print pp(rr)
