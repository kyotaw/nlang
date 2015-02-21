
import sys
from nlang.base.data.tagged_word import TaggedWord
from nlang.corpus.chasen.chasen_word import ChasenWord

def test(answer, word):
    if word.lemma != answer['lemma']:
        print('answer:' + answer['lemma'])
        print('result:' + word.lemma)
        return False
    if word.pron != answer['pron']:
        print('answer:' + answer['pron'])
        print('result:' + word.pron)
        return False
    if word.base != answer['base']:
        print('answer:' + answer['base'])
        print('result:' + word.base)
        return False
    if word.pos != answer['pos']:
        print('answer:' + answer['pos'])
        print('result:' + '-'.join(word.pos))
        return False
    if word.conj_type != answer['conj_type']:
        print('answer:' + answer['conj_type'])
        print('result:' + word.conj_type)
        return False
    if word.conj_form != answer['conj_form']:
        print('answer:' + answer['conj_form'])
        print('result:' + word.conj_form)
        return False
    if word.tag != answer['tag']:
        print('answer:' + answer['tag'])
        print('result:' + word.tag)
        return False
    if word.cost != answer['cost']:
        print('answer:' + str(answer['cost']))
        print('result:' + str(word.cost))
        return False
    if word.length != answer['length']:
        print('answer:' + str(answer['length']))
        print('result:' + str(word.length))
        return False
    return True

passed = True

line = 'ある	アル	ある	動詞-自立	五段・ラ行	基本形'
cw = ChasenWord(line)
tw = TaggedWord(cw)
answer = {'lemma':'ある','pron':'アル','base':'ある','pos':['動詞','自立'],'conj_form':'基本形','conj_type':'五段・ラ行', 'tag':'V-I-GODAN/RA-B', 'cost':sys.maxsize,'length':2}

if not test(answer, tw):
    print('failed : test1')
    passed = False

data = {'lemma':'ある','pron':'アル','base':'ある','pos':['動詞','自立'],'conj_form':'基本形','conj_type':'五段・ラ行', 'tag':'V-I-GODAN/RA-B', 'cost':100,'length':100}
tw = TaggedWord(data)
answer = data
if not test(answer, tw):
    print('failed : test2')
    passed = False

data = {'lemma':'ある','pron':'アル','base':'ある','pos':['動詞','自立'],'conj_form':'基本形','conj_type':'五段・ラ行', 'tag':'V-I-GODAN/RA-B', 'cost':100,}
tw = TaggedWord(data)
answer = {'lemma':'ある','pron':'アル','base':'ある','pos':['動詞','自立'],'conj_form':'基本形','conj_type':'五段・ラ行', 'tag':'V-I-GODAN/RA-B', 'cost':100, 'length':2}
if not test(answer, tw):
    print('failed : test3')
    passed = False

data = {'lemma':'ある','pron':'アル','base':'ある','pos':['動詞','自立'],'conj_form':'基本形','conj_type':'五段・ラ行', 'cost':100,}
tw = TaggedWord(data)
answer = {'lemma':'ある','pron':'アル','base':'ある','pos':['動詞','自立'],'conj_form':'基本形','conj_type':'五段・ラ行', 'tag':'V-I-GODAN/RA-B', 'cost':100, 'length':2}
if not test(answer, tw):
    print('failed : test4')
    passed = False

data = {'lemma':'ある','pron':'アル','base':'ある','pos':['動詞','自立'],'conj_form':'基本形','conj_type':'五段・ラ行'}
tw = TaggedWord(data)
answer = {'lemma':'ある','pron':'アル','base':'ある','pos':['動詞','自立'],'conj_form':'基本形','conj_type':'五段・ラ行', 'tag':'V-I-GODAN/RA-B', 'cost':sys.maxsize, 'length':2}
if not test(answer, tw):
    print('failed : test5')
    passed = False

if passed:
    print('all passed !!')

