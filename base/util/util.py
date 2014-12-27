# -*- coding: utf-8 -*-

import re, pprint

def pp(data):
	pp = pprint.PrettyPrinter(indent=4, width=160)
	str = pp.pformat(data)
	return re.sub(r"\\u([0-9a-f]{4})", lambda x: unichr(int("0x"+x.group(1), 16)), str)
