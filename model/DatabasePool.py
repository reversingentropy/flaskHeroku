from flask import Flask, jsonify,request
from mysql.connector import pooling,Error
from config.Settings import Settings



class DatabasePool:
    #class variable
    connection_pool = pooling.MySQLConnectionPool(
        pool_name = "ws_pool",
        pool_size=5,
        host=Settings.host,
        database=Settings.database,
        user=Settings.user,
        password=Settings.password)

    
    @classmethod
    def getConnection(cls):     
        dbConn = cls.connection_pool.get_connection()

        return dbConn

