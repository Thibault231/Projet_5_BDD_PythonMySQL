#coding: utf-8
import pymysql.cursors 
import pickle
import json
import pprint
import requests

class Food():
	def __init__(self):
		self.id = "none"
		self.name = "none"
		self.cat = "none"
		self.cat_id = "none"
		self.market = "none"
		self.descriptions ="none"
		self.nutriscore = "none"

class Checkpoint():
	def __init__(self):
		self.dtb_exist = False
		self.dtb_create = False
		self.main_loop = True
		self.pick_cat = False
		self.pick_food = False
		self.select_subs = False
		self.save = False

def sql_command(sql_instructions, cursor):
	sql = " %s"%sql_instructions
	cursor.execute(sql)
	cursor.commit
	return True

def api_extraction(categorie):
	r = requests.get(('https://fr.openfoodfacts.org/categorie/produits-tripiers/categorie/{}.json').format(categorie))
	file = r.json()
	food_list = []
	
	for element in file['products']:
		if ('ingredients_text_fr' in element) and len(element['ingredients_text_fr'])>5 :
			if 'nutriscore_grade' in element:
				if 'stores' in element:
					food_item = Food()
					food_item.id = (element['_id']) 
					food_item.name = (element['product_name'])
					food_item.nutriscore = (element['nutriscore_grade'].upper())
					food_item.cat = (categorie)
					food_item.cat_id = (cat_id)
					food_item.descriptions = (element['ingredients_text_fr'])
					food_item.market = (element['stores'])
					food_list.append(food_item)
	return food_list

if __name__ == "__main__":
	a = api_extraction('abats', 1)
	for element in a:
		print(element.__dict__, "\n\n")
	print("Food_item extraits= ", len(a))