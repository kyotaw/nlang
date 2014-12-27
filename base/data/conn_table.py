# -*- coding: utf-8 -*-

class ConnectivityTable:
	DISCONNECTABLE_COST = 99999

	def __init__(self, file_path):
		self.__table = {}
		with open(file_path, 'r') as f:
			line = f.readline()
			while line:
				tokens = line[:-1].split('\t')
				if len(tokens) > 0:
					left_pos = tokens[0]
					if left_pos not in self.__table:
						self.__table[left_pos] = {}

					right_pos_array = tokens[1:]
					for right_pos in right_pos_array:
						pos_info = right_pos.split(':')
						self.__table[left_pos][pos_info[0]] = int(pos_info[1])
				line = f.readline()
	
	def is_connectable(self, left_pos, right_pos):
		return left_pos in self.__table and right_pos in self.__table[left_pos]

	def cost(self, left_pos, right_pos):
		return self.__table[left_pos][right_pos] if self.is_connectable(left_pos, right_pos) else DISCONNECTABLE_COST
