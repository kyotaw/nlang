# -*- coding: utf-8 -*-

import sys
import pickle
import os
import glob
import argparse

import bz2

from nlang.processor.tokenizer import Tokenizer


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--src_root_path', nargs=None, type=str, action='store')
    parser.add_argument('-f', '--file_pattern', nargs=None, type=str, action='store')
    parser.add_argument('-c', '--train_count', nargs='?', default='20', type=int, action='store')
    args = parser.parse_args()

    tokenizer = Tokenizer(True)
    with open('tokenizer.pickle.bz2', 'wb') as f:
        pic = pickle.dumps(tokenizer)
        pac = bz2.compress(pic)
        f.write(pac)
