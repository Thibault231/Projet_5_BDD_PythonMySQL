#coding: utf-8
import pymysql.cursors  


def ask_for_db(cursor):
	sql = " SHOW DATABASES;"
	cursor.execute(sql)
	db_list = []
	for row in cursor:
		db_list.append(row.get("Database"))
	if 'pur_beurre' in db_list:
		return True
	else:
		return False
 
def connect_db(cursor):
	sql ="USE Pur_Beurre;"
	cursor.execute(sql)
	return True

def implement_request(v_category, v_food_name, v_nutriscore, v_from_market, v_url_off):
	sql="INSERT INTO Main (category, food_name, nutriscore, from_market, url_off) \
    VALUES (%(cat)s, %(food)s, %(nutri)s, %(market)s, %(url)s);"
	variables = {"cat":v_category, "food" :v_food_name, "nutri" : v_nutriscore, "market" : v_from_market,"url" : v_url_off } 
	cursor.execute(sql, variables)
	connection.commit()
	return True

def cat_request(cursor):
	sql="SELECT DISTINCT category FROM Main;"
	cursor.execute(sql)
	cat_list = []
	for row in cursor:
		cat_list.append(row.get("category"))
	return cat_list

def food_request(cursor, v_cat):
	sql="SELECT food_name, id, nutriscore FROM Main \
	 WHERE category = %s ;"
	cursor.execute(sql,v_cat)
	food_list = []
	for row in cursor:
		food_list.append((row.get("food_name"),row.get("id"), row.get("nutriscore") ))
	return food_list

def substitute_request(cursor, v_cat, v_nutri, v_id):
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

def save_request(cursor, v_substitute, v_id):
	sql = "INSERT INTO BackUp (food_name, date_request, category, substitute_name, \
	nutriscore, from_market , url_off, fk_main_id) \
	SELECT %(substitute)s, NOW(), Main.category, Main.food_name, Main.nutriscore, \
	Main.from_market , Main.url_off, Main.id \
	FROM Main \
	WHERE Main.id <=> %(food_id)s;"

	variables = {"substitute": v_substitute, "food_id": v_id }
	cursor.execute(sql, variables)
	#connection.commit()
	return True

def backup_request(cursor):
	sql = "SELECT * \
    FROM BackUp \
    ORDER BY date_request, substitute_name;"
	cursor.execute(sql)
	backup_list = []
	for row in cursor:
		backup_list.append(row)
	return backup_list

if __name__ == "__main__":
	connection = pymysql.connect(host='localhost', user='root', password='Wzk2mpbamy12@', db='pur_beurre', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
	print ("connect successful!!")

	#with connection.cursor() as cursor:
		#print(ask_for_db())
		#p = ddb_implementation('roti', 'poularde_oseille', 'C', 'la_vie_claire', 'gmail.com') 	
		#a = cat_request()
		#b = food_request('pain')
		#c = substitute_request(cursor,'pain', 'A' ,2)
		#d = save_request('baguette', 4)
		#e = backup_request()
		#print(p)
		#print(a)
		#print(b)
		#print(c)
		#print(d)
		#print(e)
		#print(len(e))
		#connection.close()