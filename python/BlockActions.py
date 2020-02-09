#coding: utf-8
import pymysql.cursors 
from python.DbCreation import *
from python.SqlRequests import *
from python.Food import *
from python.Substitute import *
from python.Checkpoint import *
from python.SessionLists import *



def block_pick_categorie(cursor, connection, session, session_list)
	id_list = ['abats', 'popcorn']
	session.dtb_exist = ask_for_db(cursor, 'pur_beurre')
	
	if not session.dtb_exist:
		session.dtb_create = db_creation(cursor, connection)
		db_implementation(cursor, connection, id_list)
	link2db = connect_db(cursor, 'pur_beurre')
	
	return session, session_list

	
		
def block_pick_categorie(cursor, connection, session, food_item, subst_item, session_list)
	while not session.pick_cat:
		session_list.cat = cat_request(cursor)
		print("\nSelectionnez une des categories suivantes par son numero d'index\n")
		print("index:  0","  pour QUITTER")
		
		for index, element in enumerate(session_list.cat):
			print("index: ", index+1,"  pour la categorie :  ", element[0].upper())
			session_list.cat_index.append(str(index+1))
		cat_select = input ("Categorie selectionnee n°= ")
		
		if cat_select == '0':
			session.pick_cat = True
			session.pick_food = True
			session.select_subs = True
			session.save = True
			session.main_loop = False
			pass
		
		elif cat_select in session_list.cat_index:
			food_item.cat = session_list.cat[int(cat_select) - 1][0]
			food_item.cat_id = session_list.cat[int(cat_select) - 1][1]
			print(food_item.cat, food_item.cat_id)
			session.pick_cat = True
		
		else:
			pass
		
		return session, food_item, subst_item, session_list
			
def block_pick_food(cursor, connection, session, food_item, subst_item, session_list)
	while not session.pick_food:
		session_list.food = food_list_request(cursor, food_item.cat_id)
		print("\nVeuillez selectionner un des aliments suivant avec son numero d'index.")
		print("index:  0","  pour QUITTER")
		
		for index, element in enumerate(session_list.food):
			print("index: ", index+1,"  pour l'aliment' :  ", element[0].upper())
			session_list.food_index.append(str(index+1))
		food_select = input ("Aliment selectionne n°= ")
		
		if cat_select == '0':
			session.pick_food = True
			session.select_subs = True
			session.save = True
			session.main_loop = False
			pass
		
		elif food_select in session_list.food_index:
			food_item = food_item_request(cursor, food_item.cat, food_item.cat_id)
			session.pick_food = True
			subst_item = substitute_request(cursor, food_item.cat, food_item.cat_id, food_item.id)
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
	
	return session, food_item, subst_item, session_list

def block_save(cursor, connection, session, food_item, subst_item, session_list)
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
	
	return session, food_item, subst_item, session_list

def block_history(cursor, connection, session, session_list)
	session_list.history = history_request(cursor, 4)
		
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

def block_hided_command(cursor, connection, session)
	sql_instructions = input("Entrez l'instruction sql avec un seul ';' >>: ")
	session.hide_command = sql_command(cursor, connection, sql_instructions)
	print("\nCommande exécutée")

	end_answer = input ("Tapez 'Q' pour QUITTER ou n'imorte quelle touche pour retourner au menu principal.\n >>:")
	
	if end_answer.lower() == "q":
		session.main_loop = False
	
	return session

