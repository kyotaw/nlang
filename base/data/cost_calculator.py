# -*- coding: utf-8 -*8

import math

def calculate_cost(probability):
	return int(round(-math.log(probability, 2) * 1000, 0) + 1000)

	
