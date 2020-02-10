#coding: utf-8

class Checkpoint():
	def __init__(self):
		self.dtb_exist  = False 
		self.dtb_create = False 
		self.main_loop = True
		self.pick_cat = False 
		self.pick_food = False 
		self.select_subs = False 
		self.save = False
		self.hide_command = False

	def checkpoint_reset(self):
		self.pick_cat = False 
		self.pick_food = False 
		self.select_subs = False 
		self.save = False
		self.hide_command = False
