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
 
def cat_request(cursor):
	""" 
	Select different kind of datas contains in the column "category" 
	from table "Main".
	Return a list object.
	Takes one argument: "cursor" for connection with Mysql.
	"""
	sql="SELECT DISTINCT cat_name, id FROM Category;"
	cursor.execute(sql)
	cat_list = []
	for row in cursor:
		cat_list.append((row.get("cat_name"), row.get("id")))
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

def food_item_request(cursor,v_cat, v_cat_id):
	""" 
	Select different kind of datas contains in the column "food_name" 
	from table "Main" for a specific food's category.
	Return a list object.
	Takes two arguments: 
	"cursor" for connection with Mysql.
	"v_cat" for the food's category
	"""
	sql="SELECT * FROM Food \
	 WHERE fk_category_id = %s ;"
	cursor.execute(sql,v_cat_id)
	food_list = []
	sql="SELECT * FROM Food \
	 WHERE fk_category_id = %s ;"
	cursor.execute(sql,v_cat_id)
	for element in cursor:
		food_item = Food()
		food_item.id = (element['id']) 
		food_item.name = (element['name'])
		food_item.nutriscore = (element['nutriscore'].upper())
		food_item.cat = v_cat
		food_item.cat_id = v_cat_id
		food_item.descriptions = (element['descriptions'])
		food_item.market = (element['market'])
		food_item.url_id = (element['url_id'])
	return food_item

def food_list_request(cursor, v_cat_id):
	""" 
	Select different kind of datas contains in the column "food_name" 
	from table "Main" for a specific food's category.
	Return a list object.
	Takes two arguments: 
	"cursor" for connection with Mysql.
	"v_cat" for the food's category
	"""
	sql="SELECT name, id FROM Food \
	 WHERE fk_category_id = %s ;"
	cursor.execute(sql,v_cat_id)
	food_list = []
	for element in cursor:
		food_list.append((element['name'],element['id']))	
	return food_list

def history_request(cursor, v_len_history):
	""" 
	Call all datas contains in the table "BackUp"
	Return a list object.
	Takes one argument: "cursor" for connection with Mysql.
	"""
	sql = "SELECT Category.cat_name, History.origin_name, History.date_request, Food.id,\
	Food.name, Food.url_id, Food.descriptions, Food.market, Food.nutriscore \
    FROM History \
    INNER JOIN Food ON Food.id = History.fk_subst_id\
    INNER JOIN Category ON Category.id = Food.fk_category_id \
    ORDER BY History.date_request, Food.id\
    LIMIT %s;"
	cursor.execute(sql, v_len_history)
	history_list = []
	for element in cursor:
		history_item = Substitute()
		history_item.date_request = (element['date_request'])
		history_item.name = (element['name'])
		history_item.origin_name = (element['origin_name'])
		history_item.cat = (element['cat_name'])
		history_item.market = (element['market'])
		history_item.nutriscore = (element['nutriscore'])
		history_item.descriptions = (element['descriptions'])
		history_list.append(history_item)
	return history_list

def implement_cat(cursor, connection, v_cat):
	sql="INSERT INTO Category (cat_name) VALUES (%s);"
	sql1 = "SELECT id FROM Category WHERE cat_name = %s LIMIT 1;"
	cursor.execute(sql, v_cat)
	connection.commit()
	cursor.execute(sql1, v_cat)
	for row in cursor:
		cat_id = row.get("id")
	return cat_id

def implement_food(cursor, connection, v_cat, v_name, v_nutriscore,v_descriptions,
v_market, v_url_id):    
	variables = {"v_cat":v_cat, "v_name":v_name, "v_nutriscore":v_nutriscore,
	"v_descriptions":v_descriptions,"v_market":v_market, "v_url_id":v_url_id}

	sql = "INSERT INTO Food (name, nutriscore, descriptions, market, url_id, fk_category_id)\
	SELECT %(v_name)s, %(v_nutriscore)s, %(v_descriptions)s, %(v_market)s, %(v_url_id)s, Category.id  \
	FROM Category \
	WHERE Category.cat_name <=> %(v_cat)s\
	LIMIT 1;"
	cursor.execute(sql, variables)
	connection.commit()
	return True

def save_request(cursor, connection, v_fk_subst_id, v_fk_category_id, v_origin_name):
	"""
	Save substitute's datas and food item's name in the table  "BackUp"
	for the current research. 
	Takes three arguments: "cursor" for connection with Mysql,
	"v_substitute, v_id" for object to save.
	"""
	sql = "INSERT INTO History (fk_subst_id, date_request, fk_category_id, origin_name) \
	VALUES (%(subst_id)s, NOW(), %(cat_id)s, %(origin_name)s );"

	variables = {"subst_id": v_fk_subst_id, "cat_id": v_fk_category_id, "origin_name": v_origin_name }
	cursor.execute(sql, variables)
	connection.commit()
	return True

def sql_command(cursor, connection, sql_instructions):
	sql = "%s"%sql_instructions
	cursor.execute(sql)
	connection.commit()
	return True

def substitute_request(cursor,v_cat, v_cat_id, v_id):
	""" 
	Select one row from the table "Main" with the same v_cat and v_nutri
	than the row indicated by v_id.
	Return a dictionnary object.
	Takes four arguments: "cursor" for connection with Mysql,
	"v_cat, v_nutri, v_id" for identifying substitute.
	"""
	sql = "SELECT * \
	FROM Food \
	WHERE fk_category_id= %(cat_id)s AND id!= %(id)s \
	ORDER BY nutriscore \
	LIMIT 1;"
	variables = {"cat_id": v_cat_id,"id": v_id}
	cursor.execute(sql, variables)
	substitute = {}
	for element in cursor:
		subst_item = Food()
		subst_item.id = (element['id']) 
		subst_item.name = (element['name'])
		subst_item.nutriscore = (element['nutriscore'].upper())
		subst_item.cat = v_cat
		subst_item.cat_id = v_cat_id
		subst_item.descriptions = (element['descriptions'])
		subst_item.market = (element['market'])
		subst_item.url_id = (element['url_id'])
	return subst_item

