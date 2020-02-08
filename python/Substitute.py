#coding: utf-8
import pymysql.cursors 
import pickle
import json
import pprint
import requests

class Substitute(Food):
	"""  Initiate characters attributs """
	def __init__(self):
		Food.__init__(self)
		self.origin_name = "none"
		self.date_request = "none"
		