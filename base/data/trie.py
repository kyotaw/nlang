class Trie:
	def __init__(self):
		self.root = {}

	def insert(self, key, value):
		self.__insert(self.root, key, value)

	def common_prefix_search(self, key):
		return self.__common_prefix_search(self.root, key)

	def dump(self):
		data = []
		key = u''
		self.__dump(self.root, key, data)
		return data

	def count(self, key, value):
		return self.__count(self.root, key, value)

	def __common_prefix_search(self, dict, key):
		data = []
		if 'value' in dict:
			for pkg in dict['value']:
				data.append(pkg['data'])
		if key:
			key_head = key[0]
			if key_head in dict:
				data += self.__common_prefix_search(dict[key_head], key[1:])
		return data
	
	def __insert(self, dict, key, value):
		if key:
			key_head = key[0]
			if key_head not in dict:
				dict[key_head] = {}
			self.__insert(dict[key_head], key[1:], value)
		else:
			if 'value' not in dict:
				dict['value'] = []
			for pkg in dict['value']:
				if value == pkg['data']:
					pkg['count'] += 1
					return
			dict['value'].append({'data':value, 'count':1})
			
	def __dump(self, dict, key, data):
		if 'value' in dict:
			for pkg in dict['value']:
				data.append(pkg['data'])
		for k, v in dict.items():
			if k != 'value':
				key = key + k
				self.__dump(v, key, data)
	
	def __count(self, dict, key, value):
		if key:
			key_head = key[0]
			if key_head not in dict:
				return 0
			return self.__count(dict[key_head], key[1:], value)
		else:
			if 'value' not in dict:
				return 0
			for pkg in dict['value']:
				if value == pkg['data']:
					return pkg['count']
			return 0 

