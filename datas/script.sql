--SOURCE C:/Users/SALGUES-BESNARD/Documents/GitHub/Projet_5_BDD_PythonMySQL/datas/script.sql;

SOURCE C:/Users/SALGUES-BESNARD/Documents/GitHub/Projet_5_BDD_PythonMySQL/datas/data.sql;

SHOW TABLES;
CALL ddb_implement_cat('creme_marron'); 
CALL ddb_implement_food('creme_marron', 'le_cremeux','A','Bon bon pour le moral', 'Auchan carrouf', '123456789');
SELECT * FROM Food;
SELECT * FROM Category;