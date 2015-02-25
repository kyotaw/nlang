# -*- coding: utf-8 -*- 

from nlang.base.util.util import pp
from nlang.processor.tokenizer import Tokenizer
from nlang.processor.chunker import Chunker

s = Tokenizer()
r = s.tag("ピエリ守山は2008年に開業。当時、県内最大の商業施設として約200店舗でスタートしましたが、景気の悪化に加え、開業数カ月後には隣接する草津市に「イオンモール草津」がオープン。")

ff = []
for f in r:
    ff.append((f.lemma, f.tag))
print(pp(ff))
c = Chunker()
rr = c.clause(r)
for clause in rr:
    lem = [w.lemma for w in clause]
    print(lem)
