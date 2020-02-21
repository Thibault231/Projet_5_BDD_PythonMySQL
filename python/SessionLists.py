# coding: utf-8
""" Rule the class 'sessionlists.SessionLists'
"""
from .substitute import Substitute


class SessionLists():
    """Class 'substitute.Substitute'
    Stock all classes 'food.Food','subsitute.Substitute' and
    'checkpoint.Checkpoint' objects
    while running program.

    Attributs (= Default):
    cat_impl = ['abats', 'taboules-aux-legumes','margarines',
    'compotes-pommes-nature','sauces-tomates-au-basilic',
    'yaourts-natures','brioches-tranchees','cereales-pour-petit-dejeuner',
    'galettes-de-riz-souffle', 'pestos-au-basilic',
    'citrons', 'biscuits', 'chocolats-noirs-sales',
    'pates-a-pizza', 'jus-d-orange']
    food: list (= empty)
    food_index: list (= empty)
    cat_index: list (= empty)
    history: list (= empty)

    Class methods:
    -cat_list_request
    -food_list_request
    -history_request
    -sessionlists_reset

    Example:
        session_list = SessionLists()
    """

    def __init__(self):
        self.cat_impl = [
            [
                'acras', 'endives-au-jambon', 'cassoulets',
                'pains-aux-raisins', 'brioches-tranchees',
                'croissants-fourres', 'yaourts-natures',
                'laits-concentres', 'milkfat', 'biscuits',
                'sauces-tomates-au-basilic', 'aiolis', 'guacamoles',
                'pizzas-au-chorizo', 'pizzas-chevre-lardons',
                'chocolats-noirs-sales', 'jus-d-orange'],
            [
                'Plats préparés', 'Viennoiseries', 'Produits laitiers',
                'Sauces', 'Pizzas', 'Snacks sucrés'
                ]
                ]
        self.food = []
        self.food_index = []
        self.cat = []
        self.cat_index = []
        self.history = []

    def cat_list_request(self, cursor):
        """ Stock all the distincts category of the tables category
        in the Pur_Beurre database in the 'cat_list' attribut of the
        'sessionlist.SessionList' object.

        Args:
        self: class 'sessionlist.SessionList'
        cursor: class 'pymysql.cursors.DictCursor'

        Return:
        /

        Example:
        self.cat_list_request(cursor)
        """
        sql = "SELECT DISTINCT cat_name, id FROM Category;"
        cursor.execute(sql)
        for row in cursor:
            self.cat.append((row.get("cat_name"), row.get("id")))

    def food_list_request(self, cursor, v_cat_id):
        """ Stock all food item's names and ids of the tables Food
        in the Pur_Beurre database, in the 'food' attribut of the
        'sessionlist.SessionList' object.
        Name and id are stocked in a tupple for each food item.

        Args:
        self: class 'sessionlist.SessionList'
        cursor: class 'pymysql.cursors.DictCursor'
        v_cat_id: int

        Return:
        /

        Example:
        self.food_list_request(cursor, v_cat_id)
        """
        sql = "SELECT food.name, food.id\
        FROM Food\
        INNER JOIN Category_Food AS cf ON cf.fk_id_food <=> food.id\
        INNER JOIN Category ON Category.id <=> cf.fk_id_category\
        WHERE Category.id = %s;"
        cursor.execute(sql, v_cat_id)
        for element in cursor:
            self.food.append((element['name'], element['id']))

    def history_request(self, cursor, v_len_history=""):
        """ Stock in the attribute 'history' an amont of 'v_len_history' object
        of class subsitute.Substitute from the tables 'History' of the
        database Pur_Beurre.

        Args:
        self: class 'sessionlist.SessionList'
        cursor: class 'pymysql.cursors.DictCursor'
        v_len_history: int (default = "")

        Return:
        /

        Example:
        self.history_request(cursor, v_len_history="")
        """
        sql = "SELECT s1.name, s1.nutriscore, s1.descriptions, s1.id, s1.market,\
        s1.url_id, History.date_request, f1.name, f1.nutriscore,\
        f1.descriptions, Category.cat_name\
        FROM History\
        INNER JOIN Food as f1 ON f1.id <=> History.fk_origin_id\
        INNER JOIN Food as s1 ON s1.id <=> History.fk_subst_id\
        INNER JOIN Category ON Category.id <=> History.fk_category_id\
        ORDER BY History.date_request, s1.id %s;" % v_len_history
        cursor.execute(sql)

        for element in cursor:
            history_item = Substitute()
            history_item.date_request = element['date_request']
            history_item.name = element['name']
            history_item.cat = element['cat_name']
            history_item.market = element['market']
            history_item.nutriscore = element['nutriscore']
            history_item.descriptions = element['descriptions']
            history_item.origin_name = element['f1.name']
            history_item.origin_nutriscore = element['f1.nutriscore']
            history_item.origin_description = element['f1.descriptions']
            self.history.append(history_item)

    def sessionlists_reset(self):
        """ Reset attributs 'food', 'food_index', cat, 'cat_index' and 'history'
        to default values (= empty list).

        Args:
        self: class 'sessionlist.SessionList'

        Return:
        /

        Example:
        self.sessionlists_reset()
        """
        self.food = []
        self.food_index = []
        self.cat = []
        self.cat_index = []
        self.history = []
