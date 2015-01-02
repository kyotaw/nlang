# -*- coding: utf-8 -*-

import os
import string
from nlang.setting import options

NLANG_ROOT = os.path.dirname(os.path.abspath(__file__))[:-11]

def connfile_path():
	option = __get_option('CONNFILE_PATH')
	return option if option != '' else NLANG_ROOT + 'data/conn/master/master.conn'

def vocabfile_path():
	option = __get_option('VOCABFILE_PATH')
	return option if option != '' else NLANG_ROOT + 'data/vocab/master/master.vocab'

def phrase_enter_connfile_path():
	option = __get_option('PHRASE_ENTER_CONNFILE_PATH')
	return option if option != '' else NLANG_ROOT + 'data/phrase/master/master.ph_enter_conn'

def phrase_exit_connfile_path():
	option = __get_option('PHRASE_EXIT_CONNFILE_PATH')
	return option if option != '' else NLANG_ROOT + 'data/phrase/master/master.ph_exit_conn'

def phrasefile_path():
	option = __get_option('PHRASEFILE_PATH')
	return option if option != '' else NLANG_ROOT + 'data/phrase/master/master.phrase'

def __get_option(item):
	return options[item] if item in options else ''

