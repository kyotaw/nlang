# -*- coding: utf-8 -*-

import os
import string
from nlang.setting import options

NLANG_ROOT = os.path.dirname(os.path.abspath(__file__))[:-11]


def connfile_path():
    option = __get_option('CONNFILE_PATH')
    return option if option != '' else NLANG_ROOT + 'data/conn/master/master.conn'


def vocabfolder_path():
    option = __get_option('VOCABFOLDER_PATH')
    return option if option != '' else NLANG_ROOT + 'data/vocab/master/'


def vocabfile_path():
    option = __get_option('VOCABFILE_PATH')
    return option if option != '' else NLANG_ROOT + 'data/vocab/master/master.vocab'

def additional_vocabfolder_path():
    option = __get_option('ADDITIONAL_VOCABFOLDER_PATH')
    return option if option != '' else NLANG_ROOT + 'data/vocab/additional/'

def clause_iob_connfile_path():
    option = __get_option('CLAUSE_IOB_CONNFILE_PATH')
    return option if option != '' else NLANG_ROOT + 'data/clause/master/master.iob_conn'


def trained_clause_iob_connfile_path():
    option = __get_option('TRAINED_CLAUSE_IOB_CONNFILE_PATH')
    return option if option != '' else NLANG_ROOT + 'data/clause/master/master.iob_conn.trained'


def clausefile_path():
    option = __get_option('CLAUSEFILE_PATH')
    return option if option != '' else NLANG_ROOT + 'data/clause/master/master.clause'


def trained_clausefile_path():
    option = __get_option('TRAINED_CLAUSEFILE_PATH')
    return option if option != '' else NLANG_ROOT + 'data/clause/master/master.clause.trained'


def ready_made_tokenizer():
    option = __get_option('READYMADE_TOKENIZER')
    return option if option != '' else NLANG_ROOT + 'data/instance/tokenizer.pickle.bz2'


def ready_made_chunker():
    option = __get_option('READYMADE_CHUNKER')
    return option if option != '' else NLANG_ROOT + 'data/instance/chunker.pickle.bz2'


def ready_made_sentencer():
    option = __get_option('READYMADE_SENTENCER')
    return option if option != '' else NLANG_ROOT + 'data/instance/sentencer.pickle.bz2'


def __get_option(item):
    return options[item] if item in options else ''
