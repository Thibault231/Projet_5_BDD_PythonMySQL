#coding: utf-8
import pymysql.cursors
from .Food import Food

class Substitute(Food):
	"""  Initiate characters attributs """
	def __init__(self):
		Food.__init__(self)
		self.origin_name = "none"
		self.date_request = "none"

	def substitute_request(self, cursor,v_cat, v_cat_id, v_id):
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
			self.id = (element['id']) 
			self.name = (element['name'])
			self.nutriscore = (element['nutriscore'].upper())
			self.cat = v_cat
			self.cat_id = v_cat_id
			self.descriptions = (element['descriptions'])
			self.market = (element['market'])
			self.url_id = (element['url_id'])
		