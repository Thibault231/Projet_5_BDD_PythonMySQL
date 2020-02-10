#coding: utf-8
import pymysql.cursors 
from .Food import Food
from .Substitute import Substitute
from .Checkpoint import Checkpoint
from .SessionLists import SessionLists

def action_db_connection(cursor, connection, session, session_list ):
	session.ask_for_db(cursor, 'pur_beurre')
	
	if not session.dtb_exist:
		session.db_creation(cursor, connection)
		session.db_implementation(cursor, connection, session_list.cat_impl)
	session.connect_db(cursor, 'pur_beurre')	
		
	return session, session_list

	
		
def action_pick_categorie(cursor, connection, session, food_item, subst_item, session_list):
	while not session.pick_cat:
		session_list.cat_list_request(cursor)
		print("\nSelectionnez une des categories suivantes par son numero d'index\n")
		print("index:  Q","  pour QUITTER")
		
		for index, element in enumerate(session_list.cat):
			print("index: ", index+1,"  pour la categorie :  ", element[0].upper())
			session_list.cat_index.append(str(index+1))
		
		cat_select = input ("Categorie selectionnee n°= ")
		
		if cat_select.lower() == 'q':
			session.pick_cat = True 
			session.pick_food = True
			session.select_subs = True 
			session.save = True
		
		elif cat_select in session_list.cat_index:
			food_item.cat = session_list.cat[int(cat_select) - 1][0]
			food_item.cat_id = session_list.cat[int(cat_select) - 1][1]
			print(food_item.cat, food_item.cat_id)
			session.pick_cat = True
		
		else:
			session_list.cat = []
			session_list.cat_index = []
		
		return session, food_item, subst_item, session_list
			
def action_pick_food(cursor, connection, session, food_item, subst_item, session_list):
	while not session.pick_food:
		session_list.food_list_request(cursor, food_item.cat_id)
		print("\nVeuillez selectionner un des aliments suivant avec son numero d'index.")
		print("index:  Q","  pour QUITTER")
		
		for index, element in enumerate(session_list.food):
			print("index: ", index+1,"  pour l'aliment' :  ", element[0].upper())
			session_list.food_index.append(str(index+1))
		
		food_select = input ("Aliment selectionne n°= ")
		
		if food_select == 'q':
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
	while not session.save:
		save_select = input ("\nVoulez vous sauvegarder votre recherche et retourner au menu principal?\n (O= oui / N= non / Q= QUITTER) >>: ")
		
		if save_select.lower() == "o":
			print(subst_item.id, subst_item.cat_id,food_item.id)
			session.save_request(cursor, connection, subst_item.id, subst_item.cat_id, food_item.name)
			print("Votre recherche a bien été sauvegardée.")
		
		elif save_select.lower() == "n":
			print("\nRetour au menu principal. Votre recherche n'a pas été sauvegardée.\n\n")
			session.save = True
		
		elif save_select.lower() == "q":
			session.main_loop = False
		
		else:
			print("Veuillez selectionner 'O', 'N' ou 'Q'.")
	
	return session, food_item, subst_item, session_list

def action_history(cursor, connection, session, session_list):
	session_list.history_request(cursor, 4)
		
	for element in session_list.history:
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

	return session, session_list

def action_hided_command(cursor, connection, session):
	while not session.hide_command:
		sql_instructions = input("Entrez l'instruction sql avec un seul ';' ou Q pour QUITTER.\n >>: ")

		if sql_instructions.lower() == "q":
			session.hide_command = True
			session.main_loop = False
		
		else:
			sql_message = session.sql_command(cursor, connection, sql_instructions)
			print("\nCommande exécutée\n", sql_message)

	return session
