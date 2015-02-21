# -*- coding: utf-8 -*-

import re
import pprint
from nlang.base.util.unicode_util import is_ascii, is_kanji, is_hiragana, is_alpha_zenkaku, is_katakana_zenkaku, is_katakana_hankaku


def pp(data):
    pp = pprint.PrettyPrinter(indent=4, width=160)
    string = pp.pformat(data)
    return re.sub(r"\\u([0-9a-f]{4})", lambda x: unichr(int("0x" + x.group(1), 16)), string)


def get_char_type(c):
    if is_ascii(c):
        return 'ascii'
    if is_alpha_zenkaku(c):
        return 'alpha_zenkaku'
    if is_hiragana(c):
        return 'hiragana'
    if is_katakana_zenkaku(c):
        return 'katakana_zenkaku'
    if is_katakana_hankaku(c):
        return 'katakana_hankaku'
    if is_kanji(c):
        return 'kanji'

    return 'unknown'
