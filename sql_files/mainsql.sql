-- create database
DROP DATABASE IF EXISTS Pur_Beurre;
CREATE DATABASE Pur_Beurre CHARACTER SET 'UTF8MB4';
USE Pur_Beurre;

-- create tables
CREATE TABLE Main (
  id INT UNSIGNED NOT NULL AUTO_INCREMENT,
  category varchar(50) NOT NULL,
  food_name varchar(100) DEFAULT NULL,
  nutriscore CHAR(1) NOT NULL,
  from_market varchar(200) DEFAULT NULL,
  url_off varchar(200) DEFAULT NULL,
  PRIMARY KEY (id)
) ENGINE=InnoDB;

CREATE TABLE BackUp (
  back_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
  food_name varchar(100) DEFAULT NULL,
  category varchar(50) NOT NULL,
  substitute_name varchar(100) DEFAULT NULL,
  nutriscore CHAR(1) NOT NULL,
  from_market varchar(200) DEFAULT NULL,
  url_off varchar(200) DEFAULT NULL,
  date_request DATETIME DEFAULT NOW(),
  fk_main_id INT UNSIGNED NOT NULL,
  PRIMARY KEY (back_id)
) ENGINE=InnoDB;

-- create indexs
CREATE INDEX index_cat_name_nutri
ON Main (category, food_name, nutriscore, id);

-- create foreignkeys
ALTER TABLE BackUp
ADD FOREIGN KEY (fk_main_id) REFERENCES Main(id)
ON DELETE SET NULL   
ON UPDATE CASCADE; 
