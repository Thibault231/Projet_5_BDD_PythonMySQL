--SOURCE C:/Users/SALGUES-BESNARD/Documents/GitHub/Projet_5_BDD_PythonMySQL/data/script.sql;

SOURCE C:/Users/SALGUES-BESNARD/Documents/GitHub/Projet_5_BDD_PythonMySQL/data/mainsql.sql;
SOURCE C:/Users/SALGUES-BESNARD/Documents/GitHub/Projet_5_BDD_PythonMySQL/data/requests.sql
SET NAMES utf8;

SHOW TABLES;

CALL ddb_implementation('pain', 'baguette', 'B', 'leclerc', 'bof'); 
CALL ddb_implementation('pain', 'baguette', 'A', 'leclerc', 'bof');
CALL ddb_implementation('pain', 'baguetton', 'B', 'leclerc', 'bof'); 
CALL ddb_implementation('pain', 'baguetton', 'A', 'leclerc', 'bof');
CALL ddb_implementation('pain', 'baguettou', 'B', 'leclerc', 'bof'); 
CALL ddb_implementation('pain', 'baguettou', 'A', 'leclerc', 'bof');
CALL ddb_implementation('croissant', 'baguetton', 'B', 'leclerc', 'bof');
CALL ddb_implementation('croissant', 'baguetton', 'A', 'leclerc', 'bof');
CALL ddb_implementation('choco', 'baguettou', 'B', 'leclerc', 'bof'); 
CALL ddb_implementation('choco', 'baguettou', 'A', 'leclerc', 'bof');
SELECT * FROM Main; 

CALL category_request();
CALL food_request('pain');
CALL substitute_request('pain', 4, 'A');

CALL save_request('panini', 3);
CALL save_request('paneton', 6);

CALL display_old_request();

