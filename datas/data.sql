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
