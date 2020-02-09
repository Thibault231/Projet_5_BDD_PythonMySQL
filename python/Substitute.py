#coding: utf-8
from .Food import Food

class Substitute(Food):
	"""  Initiate characters attributs """
	def __init__(self):
		Food.__init__(self)
		self.origin_name = "none"
		self.date_request = "none"
		