#coding: utf-8
import pymysql.cursors 
from .Substitute import Substitute

class SessionLists():
	def __init__(self):
		self.cat_impl = ['abats', 'popcorn','margarines','boudins-noirs','cremes-de-marrons',
		'yaourts-natures','taboules','cereales-pour-petit-dejeuner','galettes-de-riz-souffle', 'sauces-tomate',
		'citrons', 'biscuits-au-chocolat', 'chocolats-noirs', 'pates-brisees', 'jus-d-orange']
		self.food = []
		self.food_index = []
		self.cat =[]
		self.cat_index = []
		self.history = []

	def cat_list_request(self, cursor):
		""" 
		Select different kind of datas contains in the column "category" 
		from table "Main".
		Return a list object.
		Takes one argument: "cursor" for connection with Mysql.
		"""
		sql="SELECT DISTINCT cat_name, id FROM Category;"
		cursor.execute(sql)
		for row in cursor:
			self.cat.append((row.get("cat_name"), row.get("id")))

	def food_list_request(self, cursor, v_cat_id):
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
		for element in cursor:
			self.food.append((element['name'],element['id']))	

	def history_request(self, cursor, v_len_history=""):
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
	    %s;"%v_len_history
		cursor.execute(sql)
		for element in cursor:
			history_item = Substitute()
			history_item.date_request = (element['date_request'])
			history_item.name = (element['name'])
			history_item.origin_name = (element['origin_name'])
			history_item.cat = (element['cat_name'])
			history_item.market = (element['market'])
			history_item.nutriscore = (element['nutriscore'])
			history_item.descriptions = (element['descriptions'])
			self.history.append(history_item)

	def sessionlists_reset(self):
		self.food = []
		self.food_index = []
		self.cat =[]
		self.cat_index = []
		self.history = []