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
    def __init__(self):
        return

    def __enter__(self):
        while True:
            try:
                self.conn = cnxpool.get_connection()
                self.curr = self.conn.cursor(dictionary=True)
                return self
            except errors.PoolError:
                time.sleep(1)

    def __exit__(self, type_val, value, trace_back):
        self.curr.close()
        self.conn.close()
