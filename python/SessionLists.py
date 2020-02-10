#coding: utf-8
import pymysql.cursors 
from .substitute import Substitute

""" Rule the class 'sessionlists.SessionLists' """

class SessionLists():
	"""Class 'substitute.Substitute'
		Stock all classes 'food.Food','subsitute.Substitute' and 'checkpoint.Checkpoint' objects
		while running program.
		
		Attributs (= Default):
		cat_impl = ['abats', 'popcorn','margarines','boudins-noirs','cremes-de-marrons',
			'yaourts-natures','taboules','cereales-pour-petit-dejeuner','galettes-de-riz-souffle', 'sauces-tomate',
			'citrons', 'biscuits-au-chocolat', 'chocolats-noirs', 'pates-brisees', 'jus-d-orange']
		food: list (= empty) 
		food_index: list (= empty) 
		cat_index: list (= empty) 
		history: list (= empty) 
		
		Class methods:
			-cat_list_request
			-food_list_request
			-history_request
			-sessionlists_reset

		Example:
			session_list = SessionLists()
	"""

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
		""" Stock all the distincts category of the tables category
		in the Pur_Beurre database in the 'cat_list' attribut of the
		 'sessionlist.SessionList' object.

		 Arguments:
		 self: class 'sessionlist.SessionList'
		 cursor: class 'pymysql.cursors.DictCursor'

		 Return:
		 /

		 Example:
		 	self.cat_list_request(cursor)
		 """
		sql="SELECT DISTINCT cat_name, id FROM Category;"
		cursor.execute(sql)
		for row in cursor:
			self.cat.append((row.get("cat_name"), row.get("id")))

	def food_list_request(self, cursor, v_cat_id):
		""" Stock all food item's names and ids of the tables Food
		in the Pur_Beurre database, in the 'food' attribut of the
		 'sessionlist.SessionList' object.
		 Name and id are stocked in a tupple for each food item.

		 Arguments:
		 self: class 'sessionlist.SessionList'
		 cursor: class 'pymysql.cursors.DictCursor'
		 v_cat_id: int

		 Return:
		 /

		 Example:
		 	self.food_list_request(cursor, v_cat_id)
		 """
		sql="SELECT name, id FROM Food \
		 WHERE fk_category_id = %s ;"
		cursor.execute(sql,v_cat_id)
		for element in cursor:
			self.food.append((element['name'],element['id']))	

	def history_request(self, cursor, v_len_history=""):
		""" Stock in the attribute 'history' an amont of 'v_len_history' object 
		of class subsitute.Substitute from the tables 'History' of the 
		database Pur_Beurre.

		 Arguments:
		 self: class 'sessionlist.SessionList'
		 cursor: class 'pymysql.cursors.DictCursor'
		 v_len_history: int (default = "")

		 Return:
		 /

		 Example:
		 	self.history_request(cursor, v_len_history="")
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
		""" Reset attributs 'food', 'food_index', cat, 'cat_index' and 'history'
		to default values (= empty list).

		 Arguments:
		 self: class 'sessionlist.SessionList'

		 Return:
		 /

		 Example:
		 	self.sessionlists_reset()
		 """
		self.food = []
		self.food_index = []
		self.cat =[]
		self.cat_index = []
		self.history = []