"""
db.py: Contains all of the logic for interfacing with a MySQL/MariaDB database server
"""
import mysql.connector.pooling
from mysql.connector.pooling import errors
import time

import config

dbconfig = {
    "database": config.MYSQL_DATABASE,
    "user": config.MYSQL_USERNAME,
    "password": config.MYSQL_PASSWORD,
    "port": config.MYSQL_PORT,
    "host": config.MYSQL_HOST
}

cnxpool = mysql.connector.pooling.MySQLConnectionPool(pool_name="cnx_pool",
                                                      pool_size=config.DB_POOL_SIZE,
                                                      **dbconfig)


class Database(object):
    """
    Database
    Object holding a single database connection from the pool. This should be used with
    the "with" context manager syntax.
    """
    def __init__(self):
        """
        Initializer for Database objects. Does essentially nothing currently.
        """
        return

    def __enter__(self):
        """
        Called when a context manager is entered. Pulls a connection off the pool.
        If no connections are available this waits until one is available (blocking).
        :return: The database object
        """
        while True:
            try:
                self.conn = cnxpool.get_connection()
                self.curr = self.conn.cursor(dictionary=True)
                return self
            except errors.PoolError:
                time.sleep(1)

    def __exit__(self, type_val, value, trace_back):
        """
        Closes the cursor and connection, returning the connection to the pool.
        :param type_val: Type of exception (if any)
        :param value: The value for the exception (if any)
        :param trace_back: The exception traceback (if any)
        :return: Nothing
        """
        self.curr.close()
        self.conn.close()
