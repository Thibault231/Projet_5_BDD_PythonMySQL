#coding: utf-8
import pymysql.cursors 
import json
import pprint
import requests

def db_creation():
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


def api_supplies(id_list)
items_list = []
for element in id_list:
	r = requests.get(('https://world.openfoodfacts.org/api/v0/products/{}.json').format(element))
	file = r.json()
	usefull_data = {"v_url_off" : ''.join(['https://fr.openfoodfacts.org/produit/',element]),
	"v_from_market" : file['product']["stores"], "v_category" : file['product']["categories_tags"],
	 "v_food_name" : file['product']["product_name"], "v_nutriscore": file['product']["nutriscore_grade"]}
	items_list.append(usefull_data)
return items_list

def supplies_list_creation(element):
	implement_request(element['v_category'], element['v_food_name'], element['v_nutriscore'],
	 element['v_from_market'], element['v_url_off'])

def db_implementation(id_list):
	items_list = api_supplies(id_list)
	for element in items_list:
		supplies_list_creation(element)
	return True

if __name__ == "__main__":
	connection = pymysql.connect(host='localhost', user='root', password='Wzk2mpbamy12@', db='sys', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
	print ("connect successful!!")

	with connection.cursor() as cursor:
		a = db_creation()
		print(a)