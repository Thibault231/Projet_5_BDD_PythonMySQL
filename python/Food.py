#coding: utf-8
import pymysql.cursors

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

	def food_item_request(self, cursor,v_cat, v_cat_id):
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
			self.id = (element['id']) 
			self.name = (element['name'])
			self.nutriscore = (element['nutriscore'].upper())
			self.cat = v_cat
			self.cat_id = v_cat_id
			self.descriptions = (element['descriptions'])
			self.market = (element['market'])
			self.url_id = (element['url_id'])

	
