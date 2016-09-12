import MySQLdb
import logging
from config import DATABASE_IP as ip
from config import DATABASE_USER as user
from config import DATABASE_USER_PASS as password
from config import DATABASE_NAME as db_name


class Dborm(object):
    """Class implementing ORM for mysql data base"""
    def __init__(self):
        self.db = MySQLdb.connect(ip, user, password, db_name)
        logging.info('Starting logger for {0}'.format(db_name))
        self.logger = logging.getLogger(db_name)

    def __del__(self):
        self.db.close()

    def select(self, table_name, columns, condition=''):
        if not isinstance(table_name, str):
            raise Exception('Should set a database name')
        if not isinstance(columns, list):
            raise Exception('Should set columns names')

        cols = ', '.join(columns)
        sql = 'select {0} from {1} {2}'.format(cols, table_name, condition)

        try:
            cursor = self.db.cursor()
            cursor.execute(sql)
            return cursor.fetchall()
        except Exception as e:
            self.logger.error(e)
            return list()

    def update(self, table_name, params, condition):
        if not isinstance(table_name, str):
            raise Exception('Should set a database name')
        if not isinstance(params, dict):
            raise Exception('Should set params dict')

        dict_params = ", ".join("{}='{}'".format(k, v)
                                for k, v in params.items())
        sql = "update {0} set {1} {2}".format(table_name,
                                              dict_params,
                                              condition)

        try:
            cursor = self.db.cursor()
            cursor.execute(sql)
            self.db.commit()
            return True
        except Exception as e:
            self.logger.error(e)
            self.db.rollback()
            return False

    def insert(self, table_name, params):
        if not isinstance(table_name, str):
            raise Exception('Should set a database name')
        if not isinstance(params, dict):
            raise Exception('Should set params dict')

        keys = ", ".join("{}".format(key) for key in params)
        vals = ", ".join("'{}'".format(params[key]) for key in params)

        dict_params = "({0}) values ({1})".format(keys, vals)
        sql = "insert into {0} {1}".format(table_name, dict_params)

        try:
            cursor = self.db.cursor()
            cursor.execute(sql)
            self.db.commit()
            return cursor.lastrowid
        except Exception as e:
            self.logger.error(e)
            self.db.rollback()
            return -1

    def delete(self, table_name, params):
        if not isinstance(table_name, str):
            raise Exception('Should set a database name')
        if not isinstance(params, dict):
            raise Exception('Should set params dict')

        try:
            key = params.keys()[0]
            dict_params = "{0}={1}".format(key, params[key])
        except Exception as e:
            self.logger.error(e)

        sql = "delete from {0} where {1}".format(table_name, dict_params)

        try:
            cursor = self.db.cursor()
            cursor.execute(sql)
            self.db.commit()
            return True
        except Exception as e:
            self.logger.error(e)
            return False
