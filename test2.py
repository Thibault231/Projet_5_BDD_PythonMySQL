#coding: utf-8
import pymysql.cursors 
import pickle
from python.db_creation import *
from python.sql_requests import *
from python.newfunc import *


#create list of food items which have to be implemented
id_list = ['abats']

# Check DB pur_beurre exists. Create it if not
session = Checkpoint()
connection = pymysql.connect(host='localhost', user= 'root', password= 'Wzk2mpbamy12@', db='sys', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
with connection.cursor() as cursor:
	session.dtb_exist = ask_for_db(cursor, 'pur_beurre')
	if not session.dtb_exist:
		session.dtb_create = db_creation(cursor, connection)
		db_implementation(cursor, connection, id_list)
	link2db = connect_db(cursor, 'pur_beurre')	

	# program's main loop
	print("Welcome to Pur_Butter program")
	while session.main_loop:
		actions = input("Please select one option with the index's number. \n1= Research for a food substitute\
		 \n2= See my old researches Q= Quitt session\n      Option = ")
		
		# user start a research for a substitute
		if actions == "1":
			
			# select a category
			while not session.pick_cat:
				cat_list = cat_request(cursor)
				print("Select one of the follower food categories with its index's number\n")
				print("index:  0","  for QUITT")
				for index, element in enumerate(cat_list):
					print("index: ", index+1,"  for category:  ", element)
				cat_select = int(input ("Category selection = "))
				if 1 <= cat_select < len(cat_list)+1 and len(cat_list)!=0:
					v_cat = cat_list[cat_select - 1]
					session.pick_cat = True
				else:
					pass
			
			#select a food item
			while not session.pick_food:
				food_list = food_request(cursor, v_cat)
				print("\nPlease select one of the follower food item with its index's number\n")
				print("index:  0","  for QUITT")
				for index, element in enumerate(food_list):
					print("index: ", index+1,"  for item:  ", element[0])
				food_select = int(input ("Food item selection = "))
				if 1 <= food_select < len(food_list)+1 and len(food_list)!=0:
					v_food = food_list[food_select-1]
					session.pick_food = True
				else:
					pass
			
			#pick an appropriate substitute in the database
			v_nutri, v_id =v_food[2],v_food[1]
			substitute = substitute_request(cursor, v_cat, v_nutri, v_id)
			print ("Your food substitute is ", substitute['food_name'],\
				"\nIts nutriscore is",substitute['nutriscore'], \
				"\nYou can purchase it in", substitute['from_market'], \
				"\nFor more informations on this substitute have a look to:\n",
				substitute['url_off'], "\n")
			session.select_subs = True

			# user choose to save or not in the datagase
			while not session.save:
				save_select = input ("Do you want to save this research? (Y/N) = ")
				if save_select.lower() == "y":
					v_substitute, v_id = v_food[1], substitute['id']
					save_request(cursor, v_substitute, v_id)
					print("Your last research have been saved.\n\n")
					checkpoint = True
				elif save_select.lower() == "n":
					print("You have quitt your last research without saving.\n\n")
					session.save = True
				else:
					print("Please select 'Y' or 'N'.")
			
			# user choose to quitt or return to the begin of the loop
			end_answer = input ("Press 'Q' to quitt or any key to return to the main menu\n >>>")
			if end_answer.lower() == "q":
				session.main_loop = False

		# user want to see old research
		elif actions == "2":
			old_list = backup_request(cursor)
			for element in old_list:
				print("Research for: ",element["food_name"],
					"\nSubstitute find:",element["substitute_name"],
					"\nNutriscore:", element["nutriscore"],
					"\nPurchasable in:",element["from_market"],
					"\nMore informations on:", element["url_off"],
					"\nDate of research", element["date_request"],"\n\n" )

			end_answer = input ("Press 'Q' to quitt or any key to return to the main menu\n >>>")
			if end_answer.lower() == "q":
				session.main_loop = False
		
		# hidding command for interracting with the database.
		elif actions == "3":
			sql_instructions = [input('Insert sql instruction for only one ";"= ')]
			sql_answ = sql_command(sql_instructions, cursor)
			print("\nCommand executed =", sql_answ,"\n")

			end_answer = input ("Press 'Q' to quitt or any key to return to the main menu\n >>>")
			if end_answer.lower() == "q":
				session.main_loop = False

		# user want to quitt the program
		elif actions.lower() == "q":
			session.main_loop = False

		#invalid input. Return to the beginning of the loop
		else:
			print("Please enter 1 or 2 for answer.\n\n")

connection.close()
