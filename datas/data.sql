-- SOURCE C:/Users/SALGUES-BESNARD/Documents/GitHub/Projet_5_BDD_PythonMySQL/datas/data.sql;

-- create database
DROP DATABASE IF EXISTS Pur_Beurre;
CREATE DATABASE Pur_Beurre CHARACTER SET 'UTF8MB4';
USE Pur_Beurre;

-- create tables
CREATE TABLE Food (
  id INT UNSIGNED NOT NULL AUTO_INCREMENT,
  food_name varchar(100) DEFAULT NULL,
  nutriscore CHAR(1) NOT NULL,
  descriptions TEXT DEFAULT NULL,
  from_market varchar(200) DEFAULT NULL,
  url_id varchar(20) DEFAULT NULL,
  fk_category_id INT UNSIGNED NOT NULL,
  PRIMARY KEY (id)
) ENGINE=InnoDB;

-- create tables
CREATE TABLE Category (
  id INT UNSIGNED NOT NULL AUTO_INCREMENT,
  cat_name VARCHAR(50) NOT NULL,
  PRIMARY KEY (id)
) ENGINE=InnoDB;


CREATE TABLE SavedSubstitutes (
  id INT UNSIGNED NOT NULL AUTO_INCREMENT,
  substitute_id INT UNSIGNED NOT NULL,
  fk_food_id INT UNSIGNED NOT NULL,
  date_request DATETIME DEFAULT NOW(),
  PRIMARY KEY (saved_id)
) ENGINE=InnoDB;

-- create indexs
CREATE INDEX index_cat_name_nutri
ON Food (fk_category_id, nutriscore, food_name, id);

-- create foreignkeys
ALTER TABLE SavedSubstitutes
ADD FOREIGN KEY (fk_food_id) REFERENCES Food(id)
ON DELETE SET NULL   
ON UPDATE CASCADE; 

ALTER TABLE SavedSubstitutes
ADD FOREIGN KEY (fk_category_id) REFERENCES Category(id)
ON DELETE SET NULL   
ON UPDATE CASCADE;

ALTER TABLE Food
ADD FOREIGN KEY (fk_category_id) REFERENCES Category(id)
ON DELETE SET NULL   
ON UPDATE CASCADE;

-- show tables and index structures
DESCRIBE category;
DESCRIBE Food;
DESCRIBE SavedSubstitutes; 
SHOW INDEX FROM Food;

-- structures of procedures used in python program.
DELIMITER | 
CREATE PROCEDURE ddb_implement_cat(v_cat VARCHAR(50))      
  BEGIN
    INSERT INTO Category (cat_name) 
    VALUES (v_cat);
  END|           
DELIMITER ;

DELIMITER | 
CREATE PROCEDURE ddb_implement_food(v_cat VARCHAR(50), v_food_name VARCHAR(100), v_nutriscore CHAR (1),
v_descriptions TEXT, v_from_market VARCHAR(200), v_url_id VARCHAR(25))      
BEGIN  
    INSERT INTO Food (food_name, nutriscore, descriptions, from_market, url_id, fk_category_id)
    SELECT v_food_name, v_nutriscore, v_descriptions, v_from_market, v_url_id, Category.id  
    FROM Category 
    WHERE Category.cat_name <=> v_cat
    LIMIT 1;
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
    FROM Food
    WHERE category <=> v_cat;
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
