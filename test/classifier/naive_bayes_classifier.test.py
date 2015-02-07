# -*- coding: utf-8 -*-

from nlang.base.util.util import pp
from nlang.classifier.naive_bayes_classifier import NaiveBayesClassifier

c = NaiveBayesClassifier()

text = u'''Python	（	パイソン	）	は	，	オランダ	人	の	グイド	・	ヴァンロッサム	が	作っ	た	オープンソース	の	プログラミング	言語	。	オブジェクト指向	スクリプト	言語	の	一種	で	あり	，	Perl	と	ともに	欧米	で	広く	普及	し	て	いる	。	イギリス	の	テレビ	局 	BBC	 	が	製作	し	た	コメディ	番組	『	空飛ぶモンティパイソン	』	に	ちなんで	名付け	られ	た	。	Python	 	は	英語	で	爬虫類	の	ニシキヘビ	の	意味	で	，	Python	言語	の	マスコット	や	アイコン	として	使わ	れる	こと	が	ある	。	Python	は	汎用	の	高水準	言語	で	ある	。	プログラマ	の	生産	性	と	コード	の	信頼	性	を	重視	し	て	設計	され	て	おり	，	核	と	なる	シンタックス	および	セマンティクス	は	必要	最小限	に	抑え	られ	て	いる	反面	，	利便	性	の	高い	大規模な	標準	ライブラリ	を	備え	て	いる	。	Unicode	 	に	よる	文字列	操作	を	サポート	し	て	おり	，	日本語	処理	も	標準	で	可能	で	ある	。	多く	の	プラットフォーム	を	サポート	し	て	おり	（	動作	する	プラットフォーム	）	，	また	，	豊富	な	ドキュメント	，	豊富な	ライブラリ	が	ある	こと	から	，	産業	界	でも	利用	が	増え	つつ	ある	。'''
words = text.split('\t')
c.train(('Python', {'word':words}))

text = u'''ヘビ	（	蛇	）	は	、	爬虫	綱	有鱗	目	ヘビ	亜目	（	Serpentes	）	に	分類	さ	れる	爬虫	類	の	総称	。	体	が細長	く	、	四肢	が	ない	の	が	特徴	。	ただし	、	同様	の	形	の	動物	は	他群	にも	存在	する	。'''
words = text.split('\t')
c.train(('Snake', {'word':words}))

text = u'''Ruby	（	ルビー	）	は	，	まつもと	ゆきひろ	（	通称	Matz	）	に	より	開発	さ	れた	オブジェクト指向	スクリプト	言語	で	あり	，	従来	 	Perl	など	の	スクリプト	言語	が	用い	られ	て	きた	領域	での	オブジェクト	指向	プログラミング	を	実現	する	。	Ruby	は	当初	1993	年	2	月	24	日	に	生ま	れ	，	 1995	年	12	月	に	fj	上	で	発表	さ	れた	。	名称	の	Ruby	は	，	プログラミング	言語	Perl	が	6	月	の	誕生	石	で	ある	Pearl	（	真珠	）	と	同じ	発音	を	する	こと	から	，	まつもと	の	同僚	の	誕生	石	（	7	月	）	の	ルビー	を	取っ	て	名付け	られ	た	。'''
words = text.split('\t')
c.train(('Ruby', {'word':words}))

text = u'''ルビー	（	英	:	 Ruby	、	紅玉	）	は	、	コランダム	（	鋼玉	）	の	変種	で	ある	。	赤色	が	特徴	的	な	宝石	で	ある	。天然	ルビー	は	産地	が	アジア	に	偏っ	て	い	て	欧米	では	採れ	ない	うえ	に	、	産地	に	おいて	も	宝石	に	できる	美しい	石	が	採れる	場所	は	極めて	限定	さ	れて	おり	、	3	カラット	を	超える	大き	な	石	は	産出	量	も	少ない	。'''
words = text.split('\t')
c.train(('Gem', {'word':words}))


allpass = True

ans = 'Python'
text = u'グイド	・	ヴァンロッサム	が	作っ	た	オープンソース'
words = text.split('\t')
guess = c.classify({'word':words})
if ans != guess:
	print('Failed to guess label: ' + guess + ' answer: ' + ans)
	allpass = False

ans = 'Ruby'
text = u'Ruby	プログラミング	言語	の	Ruby	は	純粋な	オブジェクト指向	言語	です	.'
words = text.split('\t')
guess = c.classify({'word':words})
if ans != guess:
	print('Failed to guess label: ' + guess + ' answer: ' + ans)
	allpass = False

print(pp(c.informative_features(5)))

if allpass:
	print('all passed !')
