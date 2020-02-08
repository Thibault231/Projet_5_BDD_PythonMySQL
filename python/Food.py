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
		self.url_id = "none"


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