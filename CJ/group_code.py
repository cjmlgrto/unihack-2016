# This file randomly generates the group code

import datetime

def return_time():
	return datetime.datetime.now()

def hasher(key):
	key = str(key)
	index = 0
	a = 2692
	b = 8523
	table_size = 1111
	for i in range(len(key)):
		index = (a * index + ord(key[i])) % table_size
		a = a * b % (table_size-1)
	return index

def generate_code():
	return hasher(return_time())