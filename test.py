#coding: utf-8
import pymysql.cursors 
from python.db_creation import *
from python.sql_requests import *


connection = pymysql.connect(host='localhost', user= 'root', password= 'Wzk2mpbamy12@', db='sys', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
with connection.cursor() as cursor:
	pur_butter_exist = ask_for_db(cursor)
	if not pur_butter_exist:
		db_creation()
	link2db = connect_db(cursor)

	stop_session = False
	print("Welcome to Pur_Butter program")
	
	while not stop_session:
		actions = input("Please select one option with the index's number. \n1= Research for a food substitute\
		 \n2= See my old researches Q= Quitt session\n      Option = ")

		if actions == "1":
			checkpoint = False
			while not checkpoint:
				cat_list = cat_request(cursor)
				print("Select one of the follower food categories with its index's number\n")
				print("index:  0","  for QUITT")
				for index, element in enumerate(cat_list):
					print("index: ", index+1,"  for category:  ", element)
				cat_select = int(input ("Category selection = "))
				if 1 <= cat_select < len(cat_list)+1 and len(cat_list)!=0:
					v_cat = cat_list[cat_select - 1]
					checkpoint = True
				else:
					pass
			
			checkpoint = False
			while not checkpoint:
				food_list = food_request(cursor, v_cat)
				print("\nPlease select one of the follower food item with its index's number\n")
				print("index:  0","  for QUITT")
				for index, element in enumerate(food_list):
					print("index: ", index+1,"  for item:  ", element[0])
				food_select = int(input ("Food item selection = "))
				if 1 <= food_select < len(food_list)+1 and len(food_list)!=0:
					v_food = food_list[food_select-1]
					checkpoint = True
				else:
					pass
			
			print(v_food)
			print(v_cat)
			v_nutri, v_id =v_food[2],v_food[1]
			substitute = substitute_request(cursor, v_cat, v_nutri, v_id)
			print ("Your food substitute is ", substitute['food_name'],\
				"\nIts nutriscore is",substitute['nutriscore'], \
				"\nYou can purchase it in", substitute['from_market'], \
				"\nFor more informations on this substitute have a look to:\n",
				substitute['url_off'], "\n")


			checkpoint = False
			while not checkpoint:
				save_select = input ("Do you want to save this research? (Y/N) = ")
				if save_select.lower() == "y":
					v_substitute, v_id = v_food[1], substitute['id']
					save_request(cursor, v_substitute, v_id)
					print("Your last research have been saved.\n\n")
					checkpoint = True
				elif save_select.lower() == "n":
					print("You have quitt your last research without saving.\n\n")
					checkpoint = True
				else:
					print("Please select 'Y' or 'N'.")
			
			end_answer = input ("\n\nPress 'Q' to quitt or any key to return to the main menu\n >>>")
			if end_answer.lower() == "q":
				stop_session = True

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
				stop_session = True
		
		elif actions.lower() == "q":
			stop_session = True
		else:
			print("Please enter 1 or 2 for answer.\n\n")

connection.close()
