#coding: utf-8
import pymysql.cursors 
from .food import Food
from .substitute import Substitute
from .checkpoint import Checkpoint
from .sessionlists import SessionLists

"""
Rule the program for the choices that user do.
Contain six functions:
	-action_db_connection	
	-action_pick_categorie
	-action_pick_food
	-action_save
	-action_history
	-action_hided_command

Always take cursor and connection as argument for MySQL connection.
Depending on the function, take Food()/Substitute()/Checkpoint() 
or SessionLists objects as arguments.
Depending on the function, Food()/Substitute()/Checkpoint() 
or SessionLists objects are returned 

Example:
	Checkpoint, SessionList = action_db_connection(cursor, connection, Checkpoint, SessionLists)

"""

def action_db_connection(cursor, connection, session, session_list ):
	""" Controle if the database exist. If not create it and implement
	 it with datas from OpenFoodFacts

	 Args:
	 cursor: class 'pymysql.cursors.DictCursor'
	 connection: class 'pymysql.connections.Connection'
	 session: class 'checkpoint.Checkpoint'
	 session_list: classe 'sessionsist.SessionList'

	 Return:
	 session: class 'Checkpoint.Checkpoint'
	 session_list: classe 'SessionList.SessionList'

	 Example:
	 	session, session_list = action_db_connection(cursor, connection, session, session_list)
	 """
	print("Controling for existence of database 'pur_beurre'")
	session.ask_for_db(cursor, 'pur_beurre')

	if not session.dtb_exist:
		print("Database doesnt exist.\n Creation of database." )
		session.db_creation(cursor, connection)
		print("Creation of database OK.\n Implementation from OpenfoodFacts.")
		session.db_implementation(cursor, connection, session_list.cat_impl)
		print("Implementation from OpenfoodFacts OK")
	print("Connection to 'pur_beurre' database.")
	session.connect_db(cursor, 'pur_beurre')	
	print("Connection OK.")
		
	return session, session_list

	
		
def action_pick_categorie(cursor, connection, session, food_item, subst_item, session_list):
	""" Display all distint category of the table Category in Pur_Beurre database.
	Make the user do a choice between them inputing a number.
	 it with datas from OpenFoodFacts

	 Args:
	 cursor: class 'pymysql.cursors.DictCursor'
	 connection: class 'pymysql.connections.Connection'
	 session: class 'Checkpoint.Checkpoint'
	 food_item: class 'food.Food'
	 subst_item: class 'subsitute.Substitute'
	 session_list: classe 'sessionsist.SessionList'

	 Return:
	 session: class 'Checkpoint.Checkpoint'
	 food_item: class 'food.Food'
	 subst_item: class 'subsitute.Substitute'
	 session_list: classe 'sessionsist.SessionList'

	 Example:
	session, food_item, subst_item, session_list = action_pick_categorie(cursor,
	connection, session, food_item, subst_item, session_list)
	 """

	while not session.pick_cat:
		session_list.cat_list_request(cursor)
		print("\nSelectionnez une des categories suivantes par son numero d'index\n")
		print("index:  Q","  pour QUITTER")
		
		for index, element in enumerate(session_list.cat):
			print("index: ", index+1,"  pour la categorie :  ", element[0].upper())
			session_list.cat_index.append(str(index+1))
		
		cat_select = input("Categorie selectionnee n°= ")
		
		if cat_select.lower() == 'q':
			session.pick_cat = True 
			session.pick_food = True
			session.select_subs = True 
			session.save = True
		
		elif cat_select in session_list.cat_index:
			food_item.cat = session_list.cat[int(cat_select) - 1][0]
			food_item.cat_id = session_list.cat[int(cat_select) - 1][1]
			session.pick_cat = True
		
		else:
			session_list.cat = []
			session_list.cat_index = []
		
	return session, food_item, subst_item, session_list
			
def action_pick_food(cursor, connection, session, food_item, subst_item, session_list):
	""" Display all distint food item name of the table Food in Pur_Beurre database.
	Make the user do a choice between them inputing a number.
	Select the best substitute of the food item in the table Food and displays it.

	 Args:
	 cursor: class 'pymysql.cursors.DictCursor'
	 connection: class 'pymysql.connections.Connection'
	 session: class 'Checkpoint.Checkpoint'
	 food_item: class 'food.Food'
	 subst_item: class 'subsitute.Substitute'
	 session_list: classe 'sessionsist.SessionList'

	 Return:
	 session: class 'Checkpoint.Checkpoint'
	 food_item: class 'food.Food'
	 subst_item: class 'subsitute.Substitute'
	 session_list: classe 'sessionsist.SessionList'

	 Example:
	session, food_item, subst_item, session_list = action_pick_food(cursor,
	connection, session, food_item, subst_item, session_list)
	 """
	while not session.pick_food:
		session_list.food_list_request(cursor, food_item.cat_id)
		print("\nVeuillez selectionner un des aliments suivant avec son numero d'index.")
		print("index:  Q","  pour QUITTER")
		
		for index, element in enumerate(session_list.food):
			print("index: ", index+1,"  pour l'aliment' :  ", element[0].upper())
			session_list.food_index.append(str(index+1))
		
		food_select = input("Aliment selectionne n°= ")
		
		if food_select.lower() == 'q':
			session.pick_food = True
			session.select_subs = True
			session.save = True
		
		elif food_select in session_list.food_index:
			food_item.food_item_request(cursor, food_item.cat, food_item.cat_id)
			session.pick_food = True
			subst_item.substitute_request(cursor, food_item.cat, food_item.cat_id, food_item.id)
			
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
			session_list.food = []
			session_list.food_index = []
	
	return session, food_item, subst_item, session_list

def action_save(cursor, connection, session, food_item, subst_item, session_list):
	""" Propose to the user to save its research in the table 'History' of
	the Pur_Beurre database. Do it if asked.

	 Args:
	 cursor: class 'pymysql.cursors.DictCursor'
	 connection: class 'pymysql.connections.Connection'
	 session: class 'Checkpoint.Checkpoint'
	 food_item: class 'food.Food'
	 subst_item: class 'subsitute.Substitute'
	 session_list: classe 'sessionsist.SessionList'

	 Return:
	 session: class 'Checkpoint.Checkpoint'
	 food_item: class 'food.Food'
	 subst_item: class 'subsitute.Substitute'
	 session_list: classe 'sessionsist.SessionList'

	 Example:
	session, food_item, subst_item, session_list = action_save(cursor,
	connection, session, food_item, subst_item, session_list)
	 """
	while not session.save:
		save_select = input ("\nVoulez vous sauvegarder votre recherche et retourner au menu principal?\n (O= oui / N= non / Q= QUITTER) >>: ")
		
		if save_select.lower() == "o":
			print(subst_item.id, subst_item.cat_id,food_item.id)
			session.save_request(cursor, connection, subst_item.id, subst_item.cat_id, food_item.id)
			print("Votre recherche a bien été sauvegardée.")
		
		elif save_select.lower() == "n":
			print("\nRetour au menu principal. Votre recherche n'a pas été sauvegardée.\n\n")
			session.save = True
		
		elif save_select.lower() == "q":
			session.save = True
		
		else:
			print("Veuillez selectionner 'O', 'N' ou 'Q'.")
	
	return session, food_item, subst_item, session_list

def action_history(cursor, connection, session, session_list):
	""" Asked the user for the number of previous researches it want to
	be displayed. Displayed them if asked.
	Takes datas from the table 'History' of the Pur_Beurre database.

	 Args:
	 cursor: class 'pymysql.cursors.DictCursor'
	 connection: class 'pymysql.connections.Connection'
	 session: class 'Checkpoint.Checkpoint'
	 session_list: classe 'sessionsist.SessionList'

	 Return:
	 session: class 'Checkpoint.Checkpoint'
	 
	 Example:
	session = action_history(cursor, connection, session, session_list)
	 """
	while not session.history:
		len_history = input("Voulez vous afficher:\n    \
Toutes les anciennes recherches : 'T'\n    La dernière recherche : 'D'\n    Quitter : 'Q' \n>>: ")
		if len_history.lower() == 'd':
			session_list.history_request(cursor, 'LIMIT 1')
			session.history = True

		elif len_history.lower() == 't':
			session_list.history_request(cursor)
			session.history = True

		elif len_history.lower() == "q":
			session.history = True
			session.main_loop = False
		
		else:
			print("Veuillez entrer 'Q', 'D' ou 'T'.")

		for element in session_list.history:
			print("\n\nDate de la recherche: ", element.date_request,
					"\nNom de l'aliment d'origine: ", element.origin_name,
					"\nNutriscore de l'aliment d'origine: ", element.origin_nutriscore,
					"\nDescription de l'aliment d'origine: ", element.origin_description,
					"\nNom du substitut:  ", element.name,
					"\nCatégorie du substitut: ", element.cat,
					"\nNutriscore du subsitut: ", element.nutriscore,
					"\nDescription du substitut: ", element.descriptions,
					"\nMagasin où l'acheter: ", element.market,
					"\nInformations complémentaires sur: ", ("https://fr.openfoodfacts.org/produit/{}".format(element.url_id))
					)

		end_answer = input ("\nTapez 'Q' pour QUITTER ou n'imorte quelle touche pour retourner au menu principal.\n >>:")
		if end_answer.lower() == "q":
			session.main_loop = False

	return session, session_list

def action_hided_command(cursor, connection, session):
	""" Allowed user to input a MySQL command and execute it.
	Displayed MySQL response.

	 Args:
	 cursor: class 'pymysql.cursors.DictCursor'
	 connection: class 'pymysql.connections.Connection'
	 session: class 'Checkpoint.Checkpoint'
	
	 Return:
	 session: class 'Checkpoint.Checkpoint'
	 
	 Example:
	session = action_hided_command(cursor, connection, session)
	 """
	while not session.hide_command:
		sql_instructions = input("Entrez l'instruction sql avec un seul ';' ou Q pour QUITTER.\n >>: ")

		if sql_instructions.lower() == "q":
			session.hide_command = True
			session.main_loop = False
		
		else:
			sql_message = session.sql_command(cursor, connection, sql_instructions)
			print("\nCommande exécutée\n", sql_message)

	return session
