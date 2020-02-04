#coding: utf-8

def ddb_creation():
	
	tables_creation()
	connection_ddb()
	data_list = data_sort(prim_list)
	for i in data_list:
		food_item = api_call(i)
		implementation_req(food_item)