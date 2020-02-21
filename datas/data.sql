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
  PRIMARY KEY (id)
) ENGINE=InnoDB;

CREATE TABLE Category (
  id INT UNSIGNED NOT NULL AUTO_INCREMENT,
  cat_name VARCHAR(50) NOT NULL,
  PRIMARY KEY (id)
) ENGINE=InnoDB;

CREATE TABLE Category_Food (
  fk_id_category INT UNSIGNED NOT NULL,
  fk_id_food INT UNSIGNED NOT NULL,
  PRIMARY KEY (fk_id_category, fk_id_food )
) ENGINE=InnoDB;

CREATE TABLE History (
  id INT UNSIGNED NOT NULL AUTO_INCREMENT,
  fk_subst_id INT UNSIGNED NOT NULL,
  fk_category_id INT UNSIGNED NOT NULL,
  fk_food_id INT UNSIGNED NOT NULL,
  date_request DATETIME DEFAULT NOW(),
  PRIMARY KEY (id)
) ENGINE=InnoDB;

-- create indexs
CREATE INDEX index_cat_name_nutri
ON Food (nutriscore, food_name, id);

-- create foreignkeys
ALTER TABLE History
ADD FOREIGN KEY (fk_food_id) REFERENCES Food(id)
ON DELETE CASCADE 
ON UPDATE CASCADE; 

ALTER TABLE History
ADD FOREIGN KEY (fk_subst_id) REFERENCES Food(id)
ON DELETE CASCADE 
ON UPDATE CASCADE;

ALTER TABLE History
ADD FOREIGN KEY (fk_category_id) REFERENCES Category(id)
ON DELETE CASCADE  
ON UPDATE CASCADE;

ALTER TABLE Category_food
ADD FOREIGN KEY (fk_id_category) REFERENCES Category(id)
ON DELETE CASCADE 
ON UPDATE CASCADE;

ALTER TABLE Category_food
ADD FOREIGN KEY (fk_id_food) REFERENCES Food(id)
ON DELETE CASCADE 
ON UPDATE CASCADE;

-- show database structure
DESCRIBE category;
DESCRIBE Food;
DESCRIBE Category_Food;
DESCRIBE History; 
SHOW INDEX FROM Food;
SELECT COUNT(*) FROM Food;
SELECT * FROM Category_Food;
