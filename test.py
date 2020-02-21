#coding: utf-8
import pymysql.cursors
from python.food import Food
from python.substitute import Substitute
from python.checkpoint import Checkpoint
from python.sessionlists import SessionLists
import python.actions as ac

def main():
	#create list and objects for the program.
	session_list = SessionLists()
	session = Checkpoint()

	# Check DB pur_beurre exists. Create it if not
	connection = pymysql.connect(host='localhost', user= 'root', password= 'Wzk2mpbamy12@', db='sys', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
	with connection.cursor() as cursor:	
		session, session_list = ac.action_db_connection(cursor, connection, session, session_list )
		
		print("Welcome to Pur_Butter program")

		# program's main loop
		while session.main_loop:
			actions = input("\n\nQuelle action souhaitez vous effectuer?\nTapez le numéro d'index de l'action.\n1= Rechercher un substitut pour un aliment\
			\n2= Voir mes substituts enregistrés.\n Q= Quitter le programme.\nChoix de l'action' n°= ")		
			
			# user start a research for a substitute
			if actions == "1":
				food_item = Food()
				subst_item = Substitute()

				# select a category
				session, food_item, subst_item, session_list = ac.action_pick_categorie(cursor, connection, session, food_item, subst_item, session_list)
				
				#select a food item and display a substitute
				session, food_item, subst_item, session_list = ac.action_pick_food(cursor, connection, session, food_item, subst_item, session_list)
				
				# user choose to save or not in the datagase
				session, food_item, subst_item, session_list = ac.action_save(cursor, connection, session, food_item, subst_item, session_list)

			# user want to see the old researchs
			elif actions == "2":
				session, session_list = ac.action_history(cursor, connection, session, session_list)

			# user want to quitt the program
			elif actions.lower() == "q":
				session.main_loop = False

			#invalid input. Return to the beginning of the loop
			else:
				print("Veuiller selectionner Q, 1 ou 2 comme coix d'action.")
			
			session.checkpoint_reset()
			session_list.sessionlists_reset()

	connection.close()

main()