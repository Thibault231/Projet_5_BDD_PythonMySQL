#coding: utf-8
import pymysql.cursors 
import pickle
from python.db_creation import *
from python.sql_requests import *
from python.newfunc import *


#create list and objects for the program.
id_list = ['abats', 'popcorn']
session = Checkpoint()

# Check DB pur_beurre exists. Create it if not
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
		actions = input("\n\nQuelle action souhaitez vous effectuer?\nTapez le numéro d'index de l'action.\n1= Rechercher un substitut pour un aliment\
		 \n2= Voir mes substituts enregistrés.\n Q= Quitter le programme.\nChoix de l'action' n°= ")		
		
		# user start a research for a substitute
		if actions == "1":
			food_item = Food()
			subst_item = Substitute()
			# select a category
			while not session.pick_cat:
				cat_list = cat_request(cursor)
				index_list = []
				print("\nSelectionnez une des categories suivantes par son numero d'index\n")
				print("index:  0","  pour QUITTER")
				for index, element in enumerate(cat_list):
					print("index: ", index+1,"  pour la categorie :  ", element[0].upper())
					index_list.append(str(index+1))
				cat_select = input ("Categorie selectionnee n°= ")
				if cat_select == '0':
					session.pick_cat = True
					session.pick_food = True
					session.select_subs = True
					session.save = True
					session.main_loop = False
					pass
				elif cat_select in index_list:
					food_item.cat = cat_list[int(cat_select) - 1][0]
					food_item.cat_id = cat_list[int(cat_select) - 1][1]
					print(food_item.cat, food_item.cat_id)
					session.pick_cat = True
				else:
					pass
			
			#select a food item
			while not session.pick_food:
				food_list = food_list_request(cursor, food_item.cat_id)
				index_list = []
				print("\nVeuillez selectionner un des aliments suivant avec son numero d'index.")
				print("index:  0","  pour QUITTER")
				for index, element in enumerate(food_list):
					print("index: ", index+1,"  pour l'aliment' :  ", element[0].upper())
					index_list.append(str(index+1))
				food_select = input ("Aliment selectionne n°= ")
				if cat_select == '0':
					session.pick_food = True
					session.select_subs = True
					session.save = True
					session.main_loop = False
					pass
				elif food_select in index_list:
					food_item = food_item_request(cursor, food_item.cat,food_item.cat_id)
					session.pick_food = True
					subst_item = substitute_request(cursor,food_item.cat, food_item.cat_id, food_item.id)
					if food_item.nutriscore == subst_item.nutriscore:
						print("\nDésolé mais nous n'avons trouver aucun substitut avec un meilleur nutriscore.\
							\nA nutriscore équivalent nous vous proposons cependant le produit suivant.")
					print("\nNom du substitut:  ", subst_item.name,
						"\nCatégorie d'aliment: ", subst_item.cat,
						"\nMagasin où l'acheter: ", subst_item.market,
						"\nNutriscore: ", subst_item.nutriscore,
						"\nDescription du produit: ", subst_item.descriptions,
						"\nInformations complémentaires sur: ", ("https://fr.openfoodfacts.org/produit/{}".format(subst_item.url_id))
						)
					session.select_subs = True
				else:
					pass

			# user choose to save or not in the datagase
			while not session.save:
				save_select = input ("\nVoulez vous sauvegarder votre recherche et retourner au menu principal?\n (O= oui / N= non / Q= QUITTER) >>: ")
				if save_select.lower() == "o":
					print(subst_item.id, subst_item.cat_id,food_item.id)
					session.save = save_request(cursor, connection, subst_item.id, subst_item.cat_id, food_item.name)
					print("Votre recherche a bien été sauvegardée.")
				elif save_select.lower() == "n":
					print("\nRetour au menu principal. Votre recherche n'a pas été sauvegardée.\n\n")
					session.save = True
				elif save_select.lower() == "q":
					session.main_loop = False
				else:
					print("Veuillez selectionner 'O', 'N' ou 'Q'.")

		# user want to see old research
		elif actions == "2":
			history_list = history_request(cursor, 4)
			for element in history_list:
				print("\n\nDate de la recherche: ", element.date_request,
						"\nNom de l'aliment: ", element.origin_name,
						"\nNom du substitut:  ", element.name,
						"\nCatégorie d'aliment: ", element.cat,
						"\nMagasin où l'acheter: ", element.market,
						"\nNutriscore: ", element.nutriscore,
						"\nDescription du produit: ", element.descriptions,
						"\nInformations complémentaires sur: ", ("https://fr.openfoodfacts.org/produit/{}".format(element.url_id))
						)

			end_answer = input ("\nTapez 'Q' pour QUITTER ou n'imorte quelle touche pour retourner au menu principal.\n >>:")
			if end_answer.lower() == "q":
				session.main_loop = False
		
		# hidding command for interracting with the database.
		elif actions == "3":
			sql_instructions = input("Entrez l'instruction sql avec un seul ';' >>: ")
			session.hide_command = sql_command(cursor, connection, sql_instructions)
			print("\nCommande exécutée")

			end_answer = input ("Tapez 'Q' pour QUITTER ou n'imorte quelle touche pour retourner au menu principal.\n >>:")
			if end_answer.lower() == "q":
				session.main_loop = False

		# user want to quitt the program
		elif actions.lower() == "q":
			session.main_loop = False

		#invalid input. Return to the beginning of the loop
		else:
			print("Veuiller selectionner Q, 1 ou 2 comme coix d'action.")
		
		session.pick_cat = False 
		session.pick_food = False 
		session.select_subs = False 
		session.save = False
		session.hide_command = False

connection.close()
