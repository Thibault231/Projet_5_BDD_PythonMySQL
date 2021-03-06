# coding: utf-8
""" Rule the class 'substitute.Substitute'
"""
from .food import Food


class Substitute(Food):
    """
    Class 'substitute.Substitute'

    Heritance:
    -Class food.Food

    Attributs:
    origin_name(str), date_request(str)

    All attributs are default str('none')

    Class methods:
        -substitute_request

    Example:
        subst_item = Subsitute()
    """

    def __init__(self):
        super().__init__()
        self.origin_id = "none"
        self.origin_name = "none"
        self.origin_description = "none"
        self.origin_nutriscore = "none"
        self.date_request = "none"

    def substitute_request(self, cursor, v_cat, v_cat_id, v_id):
        """ Implement all Substitute object's attributs with a picking
        row of the table Food in Pur_Beurre database.

        Args:
        self: class 'substitute.Substitute'
        cursor: class 'pymysql.cursors.DictCursor'
        connection: class 'pymysql.connections.Connection'
        v_cat: str
        v_cat_id: int
        v_id: int

        Return:
        /

        Example:
            self.substitute_request(cursor,v_cat, v_cat_id, v_id)
        """
        sql = "SELECT *\
        FROM Food\
        INNER JOIN Category_Food AS cf ON cf.fk_id_food <=> food.id\
        INNER JOIN Category ON Category.id <=> cf.fk_id_category\
        WHERE Category.id= %(cat_id)s AND Food.id!= %(id)s \
        ORDER BY nutriscore\
        LIMIT 1;"

        variables = {"cat_id": v_cat_id, "id": v_id}
        cursor.execute(sql, variables)
        for element in cursor:
            self.id = (element['id'])
            self.name = (element['name'])
            self.nutriscore = (element['nutriscore'].upper())
            self.cat = v_cat
            self.cat_id = v_cat_id
            self.descriptions = (element['descriptions'])
            self.market = (element['market'])
            self.url_id = (element['url_id'])
