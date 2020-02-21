# coding: utf-8
""" Rule the class 'checkpoint.Checkpoint'
"""
import requests
from .food import Food


class Checkpoint():
    """Class 'substitute.Substitute'
    Rule all the loops and 'actions' in the main.py
    and Actions.py files.

    Attributs (= Default):
    dtb_exist  = False
    dtb_create = False
    dtb_impl = False
    connect_dtb = False
    main_loop = True
    pick_cat = False
    pick_food = False
    select_subs = False
    save = False
    history = False

    Class methods:
        -_api_extraction
        -_implement_cat
        -_implement_food
        -ask_for_db
        -checkpoint_reset
        -connect_db
        -db_creation
        -db_implementation
        -save_request
        -sql_command

    Example:
        session = Checkpoint()
    """
    def __init__(self):
        self.dtb_exist = False
        self.dtb_create = False
        self.dtb_impl = False
        self.connect_dtb = False
        self.main_loop = True
        self.pick_cat = False
        self.pick_food = False
        self.select_subs = False
        self.save = False
        self.history = False

    def _api_extraction(self, categorie, cat_id, super_cat_list):
        """
        Return a list of class food.Food objects implemented with cat_id and
        an API from OpenfoodFacts. Datas are taken from the page "categorie".

        Args:
        self: class 'checkpoint.Checkpoint'
        cursor: class 'pymysql.cursors.DictCursor'
        connection: class 'pymysql.connections.Connection'
        cat_id: int

        Return:
        food_list: list (list of "food.Food")

        Example:
            self._api_extraction(categorie, cat_id)
        """
        r = requests.get(
            ('https://fr.openfoodfacts.org/categorie/{}.json').
            format(categorie))
        file = r.json()
        food_list = []

        for element in file['products']:
            if ('ingredients_text_fr' in element)\
                    and len(element['ingredients_text_fr']) > 5:
                if 'nutriscore_grade' in element:
                    if 'stores' in element:
                        food_item = Food()
                        food_item.id = (element['_id'])
                        food_item.name = (element['product_name'])
                        food_item.nutriscore = (
                            element['nutriscore_grade'].upper())
                        food_item.cat.append(categorie)
                        food_item.cat_id = cat_id
                        food_item.descriptions = (
                            element['ingredients_text_fr'])
                        food_item.market = (element['stores'])
                        print(element['categories'].split(', '))
                        for cat_item in super_cat_list:
                            if cat_item in element['categories'].split(', '):
                                food_item.cat.append(cat_item)

                        food_list.append(food_item)
        return food_list

    def _implement_cat(self, cursor, connection, v_cat):
        """
        Insert a new row in the table Category of database Pur_Beurre
        with column name = v_cat.
        Return the id (cat_id) of this new row.

        Args:
        self: class 'checkpoint.Checkpoint'
        cursor: class 'pymysql.cursors.DictCursor'
        connection: class 'pymysql.connections.Connection'
        v_cat: str (category's name)

        Return:
        cat_id: int

        Example:
            self._implement_cat(cursor, connection, v_cat)
        """
        sql = "INSERT INTO Category (cat_name) VALUES (%s);"
        sql1 = "SELECT id FROM Category WHERE cat_name = %s LIMIT 1;"
        cursor.execute(sql, v_cat)
        connection.commit()
        cursor.execute(sql1, v_cat)
        for row in cursor:
            cat_id = row.get("id")
        return cat_id

    def _implement_food(
            self, cursor, connection, v_cat, v_name,
            v_nutriscore, v_descriptions, v_market, v_url_id):
        """
        Create a new row in the table 'Food' of Pur_Beurre database.
        Insert inside values of v_cat, v_name, v_nutriscore, v_description,
        v_market and v_url_id.

        Args:
        self: class 'checkpoint.Checkpoint'
        cursor: class 'pymysql.cursors.DictCursor'
        connection: class 'pymysql.connections.Connection'
        v_cat: str (category's name)
        v_name: str
        v_nutriscore: str
        v_descriptions: str
        v_market: str
        v_url_id: int

        Return:
        Bolean: True

        Example:
            self._implement_food(cursor, connection, v_cat, v_name,
            v_nutriscore, v_descriptions, v_market, v_url_id)
        """

        variables = {
            "v_name": v_name, "v_nutriscore": v_nutriscore,
            "v_descriptions": v_descriptions, "v_market": v_market,
            "v_url_id": v_url_id}

        sql = "INSERT INTO Food (name, nutriscore, descriptions,\
        market, url_id)\
        VALUES (%(v_name)s, %(v_nutriscore)s, %(v_descriptions)s,\
        %(v_market)s, %(v_url_id)s);"
        cursor.execute(sql, variables)
        connection.commit()

        sql = "SELECT LAST_INSERT_ID() FROM Food;"
        cursor.execute(sql)

        for row in cursor:
            for element in v_cat:
                variables = {
                    "v_cat_name": element,
                    "v_food_id": row.get('LAST_INSERT_ID()')}
                sql = "INSERT INTO Category_Food ( fk_id_food, fk_id_category)\
                SELECT %(v_food_id)s, Category.id\
                FROM Category\
                WHERE Category.cat_name <=> %(v_cat_name)s;"
                cursor.execute(sql, variables)
                connection.commit()

        return True

    def ask_for_db(self, cursor, data_base):
        """
        Ask MySQL for presence of 'db' database.
        Turn attribut 'dtb_exist' of 'checkpoint.Checkpoint' object
        to True or false depending on MySQL answer

        Args:
        self: class 'checkpoint.Checkpoint'
        cursor: class 'pymysql.cursors.DictCursor'
        db: str

        Return:
        /

        Example:
        self.ask_for_db(cursor, db)
        """
        sql = " SHOW DATABASES;"
        cursor.execute(sql)
        db_list = []
        for row in cursor:
            db_list.append(row.get("Database"))
        if data_base in db_list:
            self.dtb_exist = True
        else:
            self.dtb_exist = False

    def checkpoint_reset(self):
        """ Reset attributs 'pick_cat', 'pick_food', 'select_subs', 'save',
        'history' and 'hided_comand' to default values (= False).

        Args:
        self: class 'checkpoint.Checkpoint'

        Return:
        /

        Example:
        self.checkpoint_reset()
        """
        self.pick_cat = False
        self.pick_food = False
        self.select_subs = False
        self.save = False
        self.history = False

    def connect_db(self, cursor, data_base):
        """
        Focus MySQL on use of 'db' database.
        Turn attribut 'dtb_exist' of 'checkpoint.Checkpoint' object
        to True when done

        Args:
        self: class 'checkpoint.Checkpoint'
        cursor: class 'pymysql.cursors.DictCursor'
        db: str

        Return:
        /

        Example:
        self.connect_db(cursor, db)
        """
        sql = "USE %s;" % data_base
        cursor.execute(sql)
        self.connect_dtb = True

    def db_creation(self, cursor, connection):
        """
        Create  MySQl database  call Pur_Beurre with three tables: Food,
        Category and History.
        Turn attribut 'dtb_create' of 'checkpoint.Checkpoint' object to true
        when done.

        Args:
        self: class 'checkpoint.Checkpoint'
        cursor: class 'pymysql.cursors.DictCursor'
        connection: class 'pymysql.connections.Connection'

        Return:
        /

        Example:
        self. db_creation(cursor, connection)
        """
        sql0 = "DROP DATABASE IF EXISTS Pur_Beurre;"

        sql1 = "CREATE DATABASE Pur_Beurre CHARACTER SET 'UTF8MB4';"

        sql2 = "USE Pur_Beurre;"

        sql3 = "CREATE TABLE Food (\
        id INT UNSIGNED NOT NULL AUTO_INCREMENT,\
        name VARCHAR(100) NOT NULL,\
        nutriscore CHAR(1) NOT NULL,\
        descriptions TEXT DEFAULT NULL,\
        market VARCHAR(200) DEFAULT NULL,\
        url_id VARCHAR(20) DEFAULT NULL,\
        PRIMARY KEY (id)\
        ) ENGINE=InnoDB;"

        sql4 = "CREATE TABLE Category (\
        id INT UNSIGNED NOT NULL AUTO_INCREMENT,\
        cat_name VARCHAR(60) NOT NULL,\
        PRIMARY KEY (id)\
        ) ENGINE=InnoDB;"

        sql5 = "CREATE TABLE Category_Food (\
        fk_id_category INT UNSIGNED NOT NULL,\
        fk_id_food INT UNSIGNED NOT NULL,\
        PRIMARY KEY (fk_id_category, fk_id_food )\
        ) ENGINE=InnoDB;"

        sql6 = "CREATE TABLE History (\
        id INT UNSIGNED NOT NULL AUTO_INCREMENT,\
        fk_origin_id INT UNSIGNED NOT NULL,\
        fk_subst_id INT UNSIGNED NOT NULL,\
        fk_category_id INT UNSIGNED NOT NULL,\
        date_request DATETIME DEFAULT NOW(),\
        PRIMARY KEY (id)\
        ) ENGINE=InnoDB;"

        sql7 = "CREATE INDEX index_cat_name_nutri\
        ON Food (nutriscore, name, id);"

        sql8 = "ALTER TABLE History\
        ADD FOREIGN KEY (fk_origin_id) REFERENCES Food(id)\
        ON DELETE CASCADE\
        ON UPDATE CASCADE;"

        sql9 = "ALTER TABLE History\
        ADD FOREIGN KEY (fk_subst_id) REFERENCES Food(id)\
        ON DELETE CASCADE\
        ON UPDATE CASCADE;"

        sql10 = "ALTER TABLE History\
        ADD FOREIGN KEY (fk_category_id) REFERENCES Category(id)\
        ON DELETE CASCADE\
        ON UPDATE CASCADE;"

        sql11 = "ALTER TABLE Category_food\
        ADD FOREIGN KEY (fk_id_category) REFERENCES Category(id)\
        ON DELETE CASCADE\
        ON UPDATE CASCADE;"

        sql12 = "ALTER TABLE Category_food\
        ADD FOREIGN KEY (fk_id_food) REFERENCES Food(id)\
        ON DELETE CASCADE\
        ON UPDATE CASCADE;"

        cursor.execute(sql0)
        cursor.execute(sql1)
        cursor.execute(sql2)
        cursor.execute(sql3)
        cursor.execute(sql4)
        cursor.execute(sql5)
        cursor.execute(sql6)
        cursor.execute(sql7)
        cursor.execute(sql8)
        cursor.execute(sql9)
        cursor.execute(sql10)
        cursor.execute(sql11)
        cursor.execute(sql12)
        connection.commit()

        self.dtb_create = True

    def db_implementation(self, cursor, connection, cat_list):
        """
        Rule the imlementation of tables Food and Category of
        Pur_Beurre database.
        Use API for the table Food and cat_list for the table Category.
        Turn attribut 'dtb_impl' of 'checkpoint.Checkpoint' object to true
        when done.

        Args:
        self: class 'checkpoint.Checkpoint'
        cursor: class 'pymysql.cursors.DictCursor'
        connection: class 'pymysql.connections.Connection'
        cat_list: list of str (sql command)

        Return:
        /

        Example:
        self.db_implementation(self, cursor, connection, cat_list)
        """
        for supcat_item in cat_list[1]:
            cat_id = self._implement_cat(cursor, connection, supcat_item)
        for cat_item in cat_list[0]:
            cat_id = self._implement_cat(cursor, connection, cat_item)
            food_list = self._api_extraction(cat_item, cat_id, cat_list[1])

            for element in food_list:
                self._implement_food(
                    cursor, connection, element.cat, element.name,
                    element.nutriscore, element.descriptions, element.market,
                    element.id)
        self.dtb_impl = True

    def save_request(
            self, cursor, connection, v_fk_subst_id, v_fk_category_id,
            v_fk_origin_id):
        """
        Save substitute's id and food item's name and id in the table 'History'
        of the database Pur_beurre for the current research.
        Turn attribut 'save' of 'checkpoint.Checkpoint' object to true when
        done.

        Args:
        self: class 'checkpoint.Checkpoint'
        cursor: class 'pymysql.cursors.DictCursor'
        connection: class 'pymysql.connections.Connection'
        v_fk_subst_id: int (foreign key from table Food)
        v_fk_category_id: int (foreign key from table Category)
        v_fk_origin_id: str

        Return:
        /

        Example:
        self.save_request(cursor, connection, v_fk_subst_id,
        v_fk_category_id, v_fk_origin_id)
        """
        sql = "INSERT INTO History (fk_subst_id, date_request,\
            fk_category_id, fk_origin_id)\
        VALUES (%(subst_id)s, NOW(), %(cat_id)s, %(origin_id)s );"

        variables = {
            "subst_id": v_fk_subst_id, "cat_id": v_fk_category_id,
            "origin_id": v_fk_origin_id}
        cursor.execute(sql, variables)
        connection.commit()
        self.save = True

    def sql_command(self, cursor, connection, sql_instructions):
        """
        Transfert sql instructions from Python console to MySQL console and
        execute them.
        Return MySql returns when done.

        Args:
        self: class 'checkpoint.Checkpoint'
        cursor: class 'pymysql.cursors.DictCursor'
        connection: class 'pymysql.connections.Connection'
        sql_instructions: str (sql command)

        Return:
        sql_message: list of str objects

        Example:
        self.sql_command(cursor, connection, sql_instructions)
        """
        sql = "%s" % sql_instructions
        cursor.execute(sql)
        connection.commit()
        sql_message = []
        for element in cursor:
            sql_message.append(element)
        return sql_message
