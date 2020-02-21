# coding: utf-8
""" Rule the class 'food.Food' """


class Food():
    """
    Class 'food.Food'

    Attributs:
    id (int), name(str), cat(str), cat_id(int), market(str),
    descriptions(str), nutriscore(str), url_id(int)

    All attributs are default str('none')

    Class methods:
    -food_item_request

    Example:
    food_item = Food()
    """
    def __init__(self):
        self.id = "none"
        self.name = "none"
        self.cat = []
        self.cat_id = "none"
        self.market = "none"
        self.descriptions = "none"
        self.nutriscore = "none"
        self.url_id = "none"

    def food_item_request(self, cursor):
        """ Implement all Food object's attributs with a picking
        row of the table Food in Pur_Beurre database.

        Args:
        self: class 'food.Food'
        cursor: class 'pymysql.cursors.DictCursor'
        connection: class 'pymysql.connections.Connection'
        v_cat: str
        v_cat_id: int

        Return:
        /

        Example:
        self.food_item_request(cursor,v_cat, v_cat_id)
        """
        sql = "SELECT * FROM Food \
        WHERE food.id = %s ;"
        cursor.execute(sql, self.id)
        for element in cursor:
            self.nutriscore = (element['nutriscore'].upper())
            self.descriptions = (element['descriptions'])
            self.market = (element['market'])
            self.url_id = (element['url_id'])
