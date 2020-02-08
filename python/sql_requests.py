#coding: utf-8
import pymysql.cursors 
import pickle
import json
import pprint
import requests
from .newfunc import *
"""
Stores functions for interracting with MySQL database through python's instructions.

Contains functions:
ask_for_db
backup_request
connect_db
cat_request
food_request
implement_request
save_request
substitute_request
"""

def api_extraction(categorie, cat_id):
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
					food_item.cat = categorie
					food_item.cat_id = cat_id
					food_item.descriptions = (element['ingredients_text_fr'])
					food_item.market = (element['stores'])
					food_list.append(food_item)
	return food_list

def ask_for_db(cursor, db):
	""" 
	Check if database exist or not. 
	Return True or False depending on the case.
	Takes two argument: "cursor" for connection with Mysql.
	"db" for database wanted
	"""
	sql = " SHOW DATABASES;"
	cursor.execute(sql)
	db_list = []
	for row in cursor:
		db_list.append(row.get("Database"))
	if db in db_list:
		return True
	else:
		return False

def backup_request(cursor):
	""" 
	Call all datas contains in the table "BackUp"
	Return a list object.
	Takes one argument: "cursor" for connection with Mysql.
	"""
	sql = "SELECT * \
    FROM BackUp \
    ORDER BY date_request, substitute_name;"
	cursor.execute(sql)
	backup_list = []
	for row in cursor:
		backup_list.append(row)
	return backup_list
 
def cat_request(cursor):
	""" 
	Select different kind of datas contains in the column "category" 
	from table "Main".
	Return a list object.
	Takes one argument: "cursor" for connection with Mysql.
	"""
	sql="SELECT DISTINCT category FROM Main;"
	cursor.execute(sql)
	cat_list = []
	for row in cursor:
		cat_list.append(row.get("category"))
	return cat_list

def connect_db(cursor, db):
	""" 
	Focus MySQL on use of Pur_Beurre database.
	Return True when done.
	Takes two arguments: "cursor" for connection with Mysql.
	"db" for database wanted
	"""
	sql ="USE %s;"%db
	cursor.execute(sql)
	return True

def food_request(cursor, v_cat):
	""" 
	Select different kind of datas contains in the column "food_name" 
	from table "Main" for a specific food's category.
	Return a list object.
	Takes two arguments: 
	"cursor" for connection with Mysql.
	"v_cat" for the food's category
	"""
	sql="SELECT food_name, id, nutriscore FROM Main \
	 WHERE category = %s ;"
	cursor.execute(sql,v_cat)
	food_list = []
	for row in cursor:
		food_list.append((row.get("food_name"),row.get("id"), row.get("nutriscore") ))
	return food_list

def implement_cat(cursor, connection, v_cat):
	sql="INSERT INTO Category (cat_name) VALUES (%s);"
	sql1 = "SELECT id FROM Category WHERE cat_name = %s LIMIT 1;"
	cursor.execute(sql, v_cat)
	connection.commit()
	cursor.execute(sql1, v_cat)
	for row in cursor:
		cat_id = row.get("id")
	print(cat_id)
	return cat_id

def implement_food(cursor, connection, v_cat, v_food_name, v_nutriscore,v_descriptions,
v_market, v_url_id):    
	variables = {"v_cat":v_cat, "v_food_name":v_food_name, "v_nutriscore":v_nutriscore,
	"v_descriptions":v_descriptions,"v_market":v_market, "v_url_id":v_url_id}

	sql = "INSERT INTO Food (food_name, nutriscore, descriptions, from_market, url_id, fk_category_id)\
	SELECT %(v_food_name)s, %(v_nutriscore)s, %(v_descriptions)s, %(v_market)s, %(v_url_id)s, Category.id  \
	FROM Category \
	WHERE Category.cat_name <=> %(v_cat)s\
	LIMIT 1;"
	cursor.execute(sql, variables)
	connection.commit()
	return True

def save_request(cursor, v_substitute, v_id):
	"""
	Save substitute's datas and food item's name in the table  "BackUp"
	for the current research. 
	Takes three arguments: "cursor" for connection with Mysql,
	"v_substitute, v_id" for object to save.
	"""
	sql = "INSERT INTO BackUp (food_name, date_request, category, substitute_name, \
	nutriscore, from_market , url_off, fk_main_id) \
	SELECT %(substitute)s, NOW(), Main.category, Main.food_name, Main.nutriscore, \
	Main.from_market , Main.url_off, Main.id \
	FROM Main \
	WHERE Main.id <=> %(food_id)s;"

	variables = {"substitute": v_substitute, "food_id": v_id }
	cursor.execute(sql, variables)
	connection.commit()
	return True

def substitute_request(cursor, v_cat, v_nutri, v_id):
	""" 
	Select one row from the table "Main" with the same v_cat and v_nutri
	than the row indicated by v_id.
	Return a dictionnary object.
	Takes four arguments: "cursor" for connection with Mysql,
	"v_cat, v_nutri, v_id" for identifying substitute.
	"""
	sql = "SELECT id, category, food_name, nutriscore, from_market, url_off \
	FROM Main \
	WHERE category= %(cat)s AND nutriscore= %(nutri)s AND id!= %(fid)s \
	LIMIT 1;"
	variables = {"cat": v_cat, "nutri": v_nutri, "fid": v_id}
	cursor.execute(sql, variables)
	substitute = {}
	for row in cursor:
		substitute = row
	if len(substitute) == 0: 
		substitute = {'food_name':'none','nutriscore':'none',\
		 'from_market':'none', 'url_off':'none'}
	return substitute

def db_implementation(cursor, connection, cat_list):
	""" 
	Implement Pur_Beurre data base with datas from Open Food Fact API.
	Use a id_list for API's requests.
	Takes three arguments: cursor, connection, id_list.
	"""
	for element in cat_list:
		cat_id = implement_cat(cursor, connection, element)
		food_list = api_extraction(element, cat_id)
		for element in food_list:
			implement_food(cursor, connection, element.cat, element.name, element.nutriscore,
			element.descriptions, element.market, element.id)
	return True


if __name__ == "__main__":
	connection = pymysql.connect(host='localhost', user= 'root', password= 'Wzk2mpbamy12@', db='sys', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
	with connection.cursor() as cursor:
		a = ask_for_db(cursor, 'pur_beurre')
		print(a)
	