# -*- coding: utf-8 -*- 

import datetime

from nlang.processor.tokenizer import Tokenizer

print('start Tokenzier')
start = datetime.datetime.now()
s = Tokenizer(True)
print('end Tokenizer: ' + str((datetime.datetime.now() - start).seconds))

print('start tag')
start = datetime.datetime.now()
r = s.tag("ピエリ守山は2008年に開業。当時、県内最大の商業施設として約200店舗でスタートしましたが、景気の悪化に加え、開業数カ月後には隣接する草津市に「イオンモール草津」がオープン。")

#r = s.tag('apple')
print('end tag: ' + str((datetime.datetime.now() - start).seconds))

res = ''
for l in r:
    res += '(' + l.lemma + ', ' + l.tag + ')' + '\n' 
print(res)
