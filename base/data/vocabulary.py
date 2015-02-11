# -*- coding: utf-8 -*-

from nlang.base.data.trie import Trie
from nlang.base.data.tagged_word import TaggedWord
from nlang.base.util.util import *

class Word(object):
    def __init__(self, raw_word):
        self.__raw = raw_word

    def get_value(self):
        return self.__raw

    def get_hook(self):
        return self.__raw['pos']
    
    def get_length(self):
        return self.__raw['length']

    def is_bos(self):
        return True if self.__raw['pos'] == 'BOS' else False

    def is_eos(self):
        return True if self.__raw['pos'] == 'EOS' else False
       
    def _get_cost(self):
        return self.__raw['cost']

    def _set_cost(self, value):
        self.__raw['cost'] = value

    cost = property(_get_cost, _set_cost)

class WordVocabulary(object):
    def __init__(self, file_path):
        self.__words = Trie()
                
        self.__words.insert('BOS', TaggedWord(lemma='BOS', pron='BOS', pos='BOS', cost=0, length=1))
        self.__words.insert('EOS', TaggedWord(lemma='EOS', pron='EOS', pos='EOS', cost=0, length=1))

        with open(file_path, 'r') as f:
            line = f.readline()
            while line:
                tokens = line[:-1].split('\t')
                if len(tokens) < 5:
                    continue
                                
                cost = 0
                conj_form = ''
                conj_type = ''
                if len(tokens) == 5:
                    cost = tokens[4]
                elif len(tokens) == 7:
                    conj_form = tokens[4]
                    conj_type = tokens[5]
                    cost = tokens[6]

                word = TaggedWord(
                    lemma=tokens[0],
                    pron=tokens[1],
                    base=tokens[2],
                    pos=tokens[3],
                    conj_form=conj_form,
                    conj_type=conj_type,
                    cost=int(cost),
                    length=len(tokens[0])
                )
                self.__words.insert(word['lemma'], word)
                line = f.readline()
                        
    def extract_vocabulary(self, stream):
        words = self.__words.common_prefix_search(stream)
        if len(words) == 0 :
            words = self.__assume_unknown_word(stream)
        return [Word(w) for w in words]

    def get_bos(self):
        return self.__get_word('BOS', 'BOS') 
    
    def get_eos(self):
        return self.__get_word('EOS', 'EOS') 
    
    def __get_word(self, lemma, pos):
        not_found = Word(TaggedWord())
        cands = self.__words.common_prefix_search(lemma)
        for w in cands:
            if w['lemma'] == lemma and w['pos'] == pos:
                return Word(w)
        return not_found
    
    def __assume_unknown_word(self, stream):
        length = len(stream)
        if length == 0:
            return []
        prev_type = '' 
        last_index = 0
        for i in range(length):
            char_type = get_char_type(stream[i])
            if prev_type != '' and prev_type != char_type:
                break
            prev_type = char_type
            last_index = i

        unk_word = stream[:last_index+1]
        tagged_word = TaggedWord(lemma=unk_word, pron='UNK', base='UNK', pos='UNK', cost=10, length=len(unk_word))
        return [tagged_word]

