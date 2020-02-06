#coding: utf-8
import pymysql.cursors 
import json
import pprint
import requests
from .sql_requests import implement_request

"""
This file stores functions for creating the MySQL database
and implementing it with datas from Open Food Fact API.
Contains functions: 
db_creation(cursor, connection)
implement_request(cursor, connection, v_category, v_food_name, v_nutriscore, v_from_market, v_url_off)
supplies_list_creation(cursor, connection, element)
api_supplies(id_list)
db_implementation(cursor, connection, id_list)

"""

def db_creation(cursor, connection):
	""" 
	Create  MySQl database  call Pur_Beurre with two tables: Main and BackUp.
	Take two arguments: cursor and connection.
	Return True if succeed
	"""
	sql0 = "DROP DATABASE IF EXISTS Pur_Beurre;"
	
	sql1 ="CREATE DATABASE Pur_Beurre CHARACTER SET 'UTF8MB4';"

	sql2 ="USE Pur_Beurre;"
	
	sql3 = "CREATE TABLE Main ( \
	  id INT UNSIGNED NOT NULL AUTO_INCREMENT,\
	  category varchar(50) NOT NULL,\
	  food_name varchar(100) DEFAULT NULL,\
	  nutriscore CHAR(1) NOT NULL,\
	  from_market varchar(200) DEFAULT NULL,\
	  url_off varchar(200) DEFAULT NULL,\
	  PRIMARY KEY (id)\
	) ENGINE=InnoDB;"

	sql4 = "CREATE TABLE BackUp ( \
	  back_id INT UNSIGNED NOT NULL AUTO_INCREMENT,\
	  food_name varchar(100) DEFAULT NULL,\
	  category varchar(50) NOT NULL,\
	  substitute_name varchar(100) DEFAULT NULL,\
	  nutriscore CHAR(1) NOT NULL,\
	  from_market varchar(200) DEFAULT NULL,\
	  url_off varchar(200) DEFAULT NULL,\
	  date_request DATETIME DEFAULT NOW(),\
	  fk_main_id INT UNSIGNED NOT NULL,\
	  PRIMARY KEY (back_id)\
	) ENGINE=InnoDB;"

	sql5 = "CREATE INDEX index_cat_name_nutri \
	ON Main (category, food_name, nutriscore, id);"

	sql6 = "ALTER TABLE BackUp\
	ADD FOREIGN KEY (fk_main_id) REFERENCES Main(id)\
	ON DELETE CASCADE   \
	ON UPDATE CASCADE;"
	
	cursor.execute(sql0)
	cursor.execute(sql1)
	cursor.execute(sql2)
	cursor.execute(sql3)
	cursor.execute(sql4)
	cursor.execute(sql5)
	cursor.execute(sql6)
	connection.commit()
	return True

def _supplies_list_creation(cursor, connection, element):
	"""
	Formates datas for implement_request in MySQl's database.
	Takes three arguments: cursor, connection, element.
	"""
	implement_request(cursor, connection, element['v_category'], element['v_food_name'], element['v_nutriscore'],
	 element['v_from_market'], element['v_url_off'])

def _api_supplies(id_list):
	"""
	Import datas from OpenFoodFact API using specifical id-list.
	Select wanted datas from the import and return them in an items_list
	Takes one argument: id_list
	"""
	items_list = []
	i = 1
	for element in id_list:
		print("to implement number>", i)
		i += 1
		r = requests.get(('https://world.openfoodfacts.org/api/v0/products/{}.json').format(element))
		file = r.json()
		usefull_data = {"v_url_off" : ''.join(['https://fr.openfoodfacts.org/produit/',str(element)]),
		"v_from_market" : file["product"]["stores"], "v_category" : file["product"]["compared_to_category"][3:],
		 "v_food_name" : file["product"]["product_name"], "v_nutriscore": file["product"]["nutriscore_grade"]}
		print(usefull_data)
		items_list.append(usefull_data)
	return items_list

def db_implementation(cursor, connection, id_list):
	""" 
	Implement Pur_Beurre data base with datas from Open Food Fact API.
	Use a id_list for API's requests.
	Takes three arguments: cursor, connection, id_list.
	"""
	items_list = _api_supplies(id_list)
	for element in items_list:
		_supplies_list_creation(cursor, connection, element)
	return True

if __name__ == "__main__":
	pass