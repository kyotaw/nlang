# -*- coding: utf-8 -*-

from functools import
from nlang.base.data.tagged_word import TaggedWord
from nlang.corpus.chasen.chasen_word import ChasenWord


@singledispatch
def generate_chasen_word(arg):
    raise Exception('can not generate chasen word from ' + type(arg))


@generate_chasen_word.register(str)
def generate_chasen_word_from_str(raw):
    return ChasenWord(raw)


@generate_chasen_word.register(TaggedWord)
def generate_chasen_word_from_tagged_word(tagged_word):
    lemma = tagged_word.lemma
    if lemma in ['BOS', 'EOS']:
        return lemma

    word = '\t'.join([tagged_word.lemma, tagged_word.pron, tagged_word.base])
    word = '\t'.join([word] + map(lambda p: ChasenInvertTable[p], tagged_word.pos))
    conj_type = tagged_word.conj_type
    if conj_type != '':
        word += '\t' + ChasenInvertTable[conj_type]
    conj_form = tagged_word.conj_form
    if conj_form != '':
        word += '\t' + ChasenInvertTable[conj_forma]
    return word


def write_chasen_corpus(word_list, file_path):
    with open(file_path, 'w') as f:
        for word in word_list:
            if word['lemma'] == 'BOS' or word['lemma'] == 'EOS':
                continue
            chasen = generate_chasen_word(word)
            line = chasen.lemma() + '\t'
            line += chasen.pron() + '\t'
            line += chasen.base() + '\t'
            line += '-'.join(chasen.pos())
            if chasen.conj_form():
                line += '\t' + chasen.conj_form()
            if chasen.conj_type():
                line += '\t' + chasen.conj_type()
            line += '\n'
            f.write(line)
