# -*- coding: utf-8 -*-

ChasenTagTable = {
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
	
	u'一段':u'ICHIDAN',
	u'一段・クレル':u'ICHIDAN/KURER',
	u'一段・得ル':u'ICHIDAN/ERU',
	u'四段・ハ行':u'YODAN/HA',
	u'四段・バ行':u'YODAN/BA',
	u'五段・ラ行':u'GODAN/RA',
	u'五段・ラ行アル':u'GODAN/RA/ARU',
	u'五段・ラ行特殊':u'GODAN/RA/SP',
	u'五段・マ行':u'GODAN/MA',
	u'五段・タ行':u'GODAN/TA',
	u'五段・サ行':u'GODAN/SA',
	u'五段・ナ行':u'GODAN/NA',
	u'五段・ガ行':u'GODAN/GA',
	u'五段・バ行':u'GODAN/BA',
	u'五段・カ行イ音便':u'GODAN/KA/I',
	u'五段・カ行促音便':u'GODAN/KA/SOK',
	u'五段・カ行促音便ユク':u'GODAN/KA/SOKYUK',
	u'五段・ワ行促音便':u'GODAN/WA/SOK',
	u'五段・ワ行ウ音便':u'GODAN/WA/U',
	u'下二・タ行':u'SIMONI/TA',
	u'下二・ダ行':u'SIMONI/DA',
	u'下二・ガ行':u'SIMONI/GA',
	u'下二・マ行':u'SIMONI/MA',
	u'下二・ハ行':u'SIMONI/HA',
	u'下二・カ行':u'SIMONI/KA',
	u'下二・得':u'SIMONI/ERU',
	u'上二・ダ行':u'KAMINI/DA',
	u'上二・ハ行':u'KAMINI/HA',
	u'上ニ・得':u'KAMINI/ERU',
	u'特殊・タ':u'SP/TA',
	u'特殊・ダ':u'SP/DA',
	u'特殊・ヌ':u'SP/NU',
	u'特殊・ナイ':u'SP/NAI',
	u'特殊・タイ':u'SP/TAI',
	u'特殊・マス':u'SP/MAS',
	u'特殊・デス':u'SP/DES',
	u'特殊・ヤ':u'SP/YA',
	u'特殊・ジャ':u'SP/JYA',
	u'サ変・スル':u'SAHEN/SUR',
	u'サ変・−スル':u'SAHEN/SUR2',
	u'サ変・−ズル':u'SAHEN/ZUR',
	u'カ変・来ル':u'KAHEN/KUR',
	u'カ変・クル':u'KAHEN/KUR',
	u'ラ変':u'RAHEN',
	u'不変化型':u'NOCONJ',
	u'形容詞・アウオ段':u'ADJ/AUO',
	u'形容詞・イ段':u'ADJ/I',
	u'形容詞・イイ':u'ADJ/II',
	u'文語・ゴトシ':u'BUN/GOTOS',
	u'文語・ナリ':u'BUN/NAR',
	u'文語・ベシ':u'BUN/BES',
	u'文語・ケリ':u'BUN/KERI',
	u'文語・マジ':u'BUN/MAJI',
	u'文語・リ':u'BUN/RI',
	u'文語・ル':u'BUN/RU',
	u'文語・キ':u'BUN/KI',
	
	u'未然形':u'Z',
	u'連用形':u'Y',
	u'終止形':u'S',
	u'基本形':u'B',
	u'連体形':u'T',
	u'命令形':u'R',
	u'仮定形':u'A',
	u'文語基本形':u'BUN/B',
	u'音便基本形':u'ON/B',
	u'未然ウ接続':u'Z/UCON',
	u'未然ヌ接続':u'Z/NUCON',
	u'未然特殊':u'Z/SP',
	u'命令ｙｏ':u'R/YO',
	u'命令ｅ':u'R/E',
	u'命令ｉ':u'R/I',
	u'命令ｒｏ':u'R/RO',
	u'体言接続':u'SUBCON',
	u'体言接続特殊':u'SUBCONSP',
	u'体言接続特殊２':u'SUBCONSP2',
	u'未然レル接続':u'RERUCON',
	u'連用デ接続':u'Y/DECON',
	u'連用タ接続':u'Y/TACON',
	u'連用テ接続':u'Y/TECON',
	u'連用ニ接続':u'Y/TECON',
	u'連用ゴザイ接続':u'Y/GOZCON',
	u'ガル接続':u'GARCON',
	u'仮定縮約１':u'A/SYUKU1',
	u'仮定縮約２':u'A/SYUKU2',
	u'現代基本形':u'MODERNB',
}