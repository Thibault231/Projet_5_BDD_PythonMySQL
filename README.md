# Projet_5_BDD_PythonMySQL


GLOBAL INFORMATIONS:

                                            BDD_PythonMySQL
                                        Eat better with Pur Butter
                                       OpenClassroom's project number 5

    Sum Up: 
    BDD_PythonMySQL is a school project program proposing substitute for many food item.
    It uses Python3 and expecially Json, Requests and mysql.connector modules (Read settings section for more informations)
	This program interacts with Openfoodfact's API to implement datas in a MySQL database called "Pur_Beurre". 
    

    BDD_PythonMySQL aim to propose the user three options:
		-See a food substitute for a picking food item.
		-See previous researches.
	With the first option the user have	to pick  a food item among a large offer, stocked in the table Food of
	"Pur_Beurre" database. A substitute with a better nutriscore is returned with its name, category, nutriscore, short description,
	store for buying it and link to OpenfoodFacts web site.
    The research can at least be saved in the history table of "Pur_Beurre" database. 
	
	With second option the user choose to display the last saved research or all of them, wich are stocked in
	the table "history" of "Pur_Beurre" database.
	
	A third option is available for development of this program. It allowed to interact directly with MySQL.

    Settings:
    Settings are contained in the file "requirement.txt".

    Running program:
    For running this program, instal settings from the file "requirement.txt" then start the game with opening the file "main.py".

AUTHOR:
T.Salgues.

LICENCE:
Projet_5_BDD_PythonMySQL is a public project without any licence.

CONVENTIONS:
	MSQL code:
	 Foreign key are under the form: fk_<origin table>_><table>
	 Example: fk_category_history
	 
	 Foreign key are under the form: v_<name of the column>
	  Example: v_cat, v_id.
	 
	 Any modification of "Pur_Beurre" database have to be noted in the file
	 "data.sql" of repertory "datas"
	  
	Python code:
		Python code respect the PEP8 convention.
		Each class have its file.
		All python's filed are put in the repertory "python" exept the main.py
		
		For docstring apply the following field
		"""" <Description>
		<Arguments>
			Arg 1: type (default value, description)
			Arg 2: type (default value, description)
			...
		<Return>
			Return 1: type (default value, description)
			Return 2: type (default value, description)
			...
		<Example>
		"""

CONTRIBUTIONs:
Source code is on https://github.com/Thibault231/Projet_5_BDD_PythonMySQL.
Use a  CONTRIBUTING.md type file to contribute.

CREDITS:
Special thanks for Openclassrooms website and Openfoodfact.