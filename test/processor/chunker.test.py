# -*- coding: utf-8 -*- 

from nlang.base.util.util import pp
from nlang.processor.tokenizer import Tokenizer
from nlang.processor.chunker import Chunker

s = Tokenizer()
r = s.tag(u'新潟県妙高市西野谷の粟立山（１１９４メートル）でスノーボードをしていた男性２人が雪崩に巻き込まれた事故で、県警などの捜索隊は１８日午前１１時頃山の東側斜面で２人を発見し、その後、１人の死亡を確認した。妙高署の発表によると、死亡したのは、同県上越市東本町、会社員水野博さん（４８）。')#同市御殿山町、会社員倉重嘉之さん（３８）は命に別条はないという。一方、同県妙高市田切の赤倉観光リゾートスキー場では、１７日午後６時頃から、知人とスキーに来ていた名古屋市千種区の男性大学院生（３５）の行方が分からなくなっており、県警などが捜索している。')

ff = []
for f in r:
	ff.append((f['lemma'], f['pos']))
print pp(ff)
c = Chunker()
rr = c.clause(r)

print pp(rr)
