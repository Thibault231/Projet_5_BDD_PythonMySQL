#coding: utf-8
import pymysql.cursors  

"""
Store functions for interracting with MySQL database through python's instructions.

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


def ask_for_db(cursor):
	""" 
	Check if database exist or not. 
	Return True or False depending on the case.
	Takes one argument: "cursor" for connection with Mysql.
	"""
	sql = " SHOW DATABASES;"
	cursor.execute(sql)
	db_list = []
	for row in cursor:
		db_list.append(row.get("Database"))
	if 'pur_beurre' in db_list:
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

def connect_db(cursor):
	""" 
	Focus MySQL on use of Pur_Beurre database.
	Return True when done.
	Takes one argument: "cursor" for connection with Mysql.
	"""
	sql ="USE Pur_Beurre;"
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

def implement_request(cursor, connection, v_category, v_food_name, v_nutriscore, v_from_market, v_url_off):
	"""
	Insert a new row in the table "Main" using arguments.  
	Takes three arguments: "cursor, connection" for connection with Mysql,
	"v_category, v_food_name, v_nutriscore, v_from_market, v_url_off" for item to insert.
	"""
	sql="INSERT INTO Main (category, food_name, nutriscore, from_market, url_off) \
    VALUES (%(cat)s, %(food)s, %(nutri)s, %(market)s, %(url)s);"
	variables = {"cat":v_category, "food" :v_food_name, "nutri" : v_nutriscore, "market" : v_from_market,"url" : v_url_off } 
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


if __name__ == "__main__":
	pass