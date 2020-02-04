#coding: utf-8

connection_mysql()
ddb_exist = check_ddb()
if NOT ddb_exist:
	ddb_creation()

connection_ddb()

stop_session = FALSE
while ind_session:

	actions = input("Que souhaitez vous faire? \n 1= Requête de substitut \n \
	 2= Voir anciennes requêtes", "\n >>>")

	if actions == 1:

		cat_list = cat_request()
		print( cat_list)
		req_cat = 0
		
		while req_cat in [A, B, C, D, E]:
			req_cat = input("Choisissez une categorie en indiquant sont numéro =")

		food_list = food_request(req_cat)
		print (food_list)
		req_food = 0
		
		while req_food in [A, B, C, D, E]:
			print ("Choisissez un aliment en indiquant sont numéro =")

		sub_food = subst_request(req_food)
		print ("Votre aliment de substitution est", sub_food)

		save_resp = FALSE
		
		while save_resp:
			save_req = input ("Voulez vous sauvegarder votre requête? (O/N) = ")
			if save_req == O:
				save_request(req_food, sub_food)
				save_resp = TRUE
			elif save_req == N:
				print("Votre requête n'a pas été sauvegarder")
				save_resp = TRUE
			else:
				print("Veuillez répondre par 'O' ou 'N'.")
		save_resp = FALSE
		
		while save_resp:
			save_req = input (" Quitter la session (=1) ou Revenir au menu principal (=2) =")
			if save_req == 1:
				stop_session = TRUE
			

	elif actions = 2:
		old_req = backup_request()
		print(old_req)


