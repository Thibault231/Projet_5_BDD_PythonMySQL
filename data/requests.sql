--SOURCE C:/Users/SALGUES-BESNARD/Documents/GitHub/Projet_5_BDD_PythonMySQL/data/requests.sql;
SET NAMES utf8;

-- create procedures
DELIMITER | 
CREATE PROCEDURE ddb_implementation(v_category VARCHAR(50), v_food_name VARCHAR(100), v_nutriscore CHAR (1),
v_from_market VARCHAR(200), v_url_off VARCHAR(200))      
BEGIN
    INSERT INTO Main (category, food_name, nutriscore, from_market, url_off)
    VALUES (v_category, v_food_name, v_nutriscore, v_from_market, v_url_off);
END|           
DELIMITER ;

DELIMITER |
CREATE PROCEDURE category_request()
BEGIN
    SELECT DISTINCT category
    FROM Main;
END |
DELIMITER ;

DELIMITER |
CREATE PROCEDURE food_request(IN v_cat VARCHAR(100))
BEGIN
    SELECT food_name, category, id
    FROM Main
    WHERE category = v_cat;
END |
DELIMITER ;

DELIMITER |
CREATE PROCEDURE substitute_request(v_cat VARCHAR(100), v_id INT, v_nutri CHAR(1))
BEGIN
    SELECT id, category, food_name, nutriscore, from_market, url_off 
    FROM Main
    WHERE category= v_cat AND nutriscore= v_nutri AND id!= v_id
    LIMIT 1;
END |
DELIMITER ;

DELIMITER |
CREATE PROCEDURE save_request(v_substitute VARCHAR(100), v_id INT)
BEGIN
    INSERT INTO BackUp (food_name, date_request, category, substitute_name, nutriscore, from_market , url_off, fk_main_id)
    SELECT v_substitute, NOW(), Main.category, Main.food_name, Main.nutriscore, Main.from_market , Main.url_off, Main.id 
    FROM Main 
    WHERE Main.id <=> v_id;
END |
DELIMITER ;


DELIMITER |
CREATE PROCEDURE display_old_request()
BEGIN
    SELECT * 
    FROM BackUp
    ORDER BY date_request, substitute_name;
END |
DELIMITER ;
