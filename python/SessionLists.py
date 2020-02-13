#coding: utf-8
import pymysql.cursors 
from .substitute import Substitute

""" Rule the class 'sessionlists.SessionLists' """

class SessionLists():
	"""Class 'substitute.Substitute'
		Stock all classes 'food.Food','subsitute.Substitute' and 'checkpoint.Checkpoint' objects
		while running program.
		
		Attributs (= Default):
		cat_impl = ['abats', 'taboules-aux-legumes','margarines','compotes-pommes-nature','sauces-tomates-au-basilic',
		'yaourts-natures','brioches-tranchees','cereales-pour-petit-dejeuner','galettes-de-riz-souffle', 'pestos-au-basilic',
		'citrons', 'biscuits-au-chocolat', 'chocolats-noirs-sales', 'pates-a-pizza', 'jus-d-orange']
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
		self.cat_impl = ['abats', 'taboules-aux-legumes','margarines','compotes-pommes-nature','sauces-tomates-au-basilic',
		'yaourts-natures','brioches-tranchees','cereales-pour-petit-dejeuner','galettes-de-riz-souffle', 'pestos-au-basilic',
		'citrons', 'biscuits-au-chocolat', 'chocolats-noirs-sales', 'pates-a-pizza', 'jus-d-orange']
		self.food = []
		self.food_index = []
		self.cat =[]
		self.cat_index = []
		self.history = []

	def cat_list_request(self, cursor):
		""" Stock all the distincts category of the tables category
		in the Pur_Beurre database in the 'cat_list' attribut of the
		 'sessionlist.SessionList' object.

		 Args:
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

		 Args:
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

		 Args:
		 self: class 'sessionlist.SessionList'
		 cursor: class 'pymysql.cursors.DictCursor'
		 v_len_history: int (default = "")

		 Return:
		 /

		 Example:
		 	self.history_request(cursor, v_len_history="")
		 """
		sql = "SELECT Food.name, Food.nutriscore, Food.descriptions, Category.cat_name,\
		History.date_request, Food.id, Food.market, Food.url_id\
	    FROM History \
	    INNER JOIN Food ON (Food.id = History.fk_subst_id)\
	    INNER JOIN Category ON Category.id = Food.fk_category_id \
	    ORDER BY History.date_request, Food.id\
	    %s;"%v_len_history
		cursor.execute(sql)
		subst_list = []
		for element in cursor:
			subst_list.append([element['date_request'], element['name'], element['cat_name'],
			element['market'], element['nutriscore'], element['descriptions']])

		sq2 = "SELECT Food.name, Food.nutriscore, Food.descriptions\
		FROM History \
		INNER JOIN Food ON (Food.id = History.fk_origin_id), History.date_request, Food.id\
		ORDER BY History.date_request, Food.id\
		%s;"%v_len_history
		cursor.execute(sq2)
		origin_list = []
		for element in cursor:
			origin_list.append([element['name'], element['nutriscore'], element['descriptions']])
			
		for rank in range(len(subst_list)):
			history_item = Substitute()
			history_item.date_request = subst_list[rank-1][0]
			history_item.name =  subst_list[rank-1][1]
			history_item.cat =  subst_list[rank-1][2]
			history_item.market =  subst_list[rank-1][3]
			history_item.nutriscore =  subst_list[rank-1][4]
			history_item.descriptions =  subst_list[rank-1][5]
			history_item.origin_name = origin_list[rank-1][0]
			history_item.origin_nutriscore  = origin_list[rank-1][1]
			history_item.origin_description = origin_list[rank-1][2]
			self.history.append(history_item)




	def sessionlists_reset(self):
		""" Reset attributs 'food', 'food_index', cat, 'cat_index' and 'history'
		to default values (= empty list).

		 Args:
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