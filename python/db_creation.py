#coding: utf-8
import pymysql.cursors 
import json
import pprint
import requests


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
	
	sql3 = "CREATE TABLE Food (\
	id INT UNSIGNED NOT NULL AUTO_INCREMENT,\
	food_name varchar(100) DEFAULT NULL,\
	nutriscore CHAR(1) NOT NULL,\
	descriptions TEXT DEFAULT NULL,\
	from_market varchar(200) DEFAULT NULL,\
	url_id varchar(20) DEFAULT NULL,\
	fk_category_id INT UNSIGNED NOT NULL,\
	PRIMARY KEY (id)\
	) ENGINE=InnoDB;"

	sql4 = "CREATE TABLE Category (\
	id INT UNSIGNED NOT NULL AUTO_INCREMENT,\
	cat_name VARCHAR(50) NOT NULL,\
	PRIMARY KEY (id)\
	) ENGINE=InnoDB;"

	sql5 = "CREATE TABLE SavedSubstitutes (\
	id INT UNSIGNED NOT NULL AUTO_INCREMENT,\
	substitute_id INT UNSIGNED NOT NULL,\
	fk_food_id INT UNSIGNED NOT NULL,\
	fk_category_id INT UNSIGNED NOT NULL,\
	date_request DATETIME DEFAULT NOW(),\
	PRIMARY KEY (id)\
	) ENGINE=InnoDB;"

	sql6 = "CREATE INDEX index_cat_name_nutri\
	ON Food (fk_category_id, nutriscore, food_name, id);"

	sql7 = "ALTER TABLE SavedSubstitutes\
	ADD FOREIGN KEY (fk_food_id) REFERENCES Food(id)\
	ON DELETE CASCADE   \
	ON UPDATE CASCADE;"
	
	sql8 = "ALTER TABLE SavedSubstitutes\
	ADD FOREIGN KEY (fk_category_id) REFERENCES Category(id)\
	ON DELETE CASCADE   \
	ON UPDATE CASCADE;"
	
	sql9 = "ALTER TABLE Food\
	ADD FOREIGN KEY (fk_category_id) REFERENCES Category(id)\
	ON DELETE CASCADE   \
	ON UPDATE CASCADE;"

	cursor.execute(sql0) 
	cursor.execute(sql1) 
	cursor.execute(sql2)
	cursor.execute(sql3)
	cursor.execute(sql4)
	cursor.execute(sql5)
	cursor.execute(sql6)
	cursor.execute(sql7)
	cursor.execute(sql8) 
	cursor.execute(sql9)
	connection.commit()
	return True



if __name__ == "__main__":
	pass