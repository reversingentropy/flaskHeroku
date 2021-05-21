from model.DatabasePool import DatabasePool
from config.Settings import Settings
import jwt
import datetime
import bcrypt

class User:
    @classmethod
    def getUser(cls,userid):
        try:
            dbConn = DatabasePool.getConnection()
            cursor = dbConn.cursor(dictionary=True)
            sql = 'select * from user where userid=%s'
            cursor.execute(sql,(userid,))
            users = cursor.fetchall()
            return users
        finally:
            dbConn.close()
    @classmethod
    def getAllUsers(cls):
        try:
            dbConn = DatabasePool.getConnection()
            cursor = dbConn.cursor(dictionary=True)
            sql = "select * from user"
            cursor.execute(sql)
            users = cursor.fetchall()
            return users
        finally:
            dbConn.close()
    
    @classmethod
    def insertUser(cls,userJSON):
        try:
            dbConn = DatabasePool.getConnection()
            cursor = dbConn.cursor(dictionary=True)
            password = userJSON['password'].encode()
            hashed = bcrypt.hashpw(password,bcrypt.gensalt())
            sql = "insert into user(username,email,role,password) values (%s,%s,%s,%s)"
            users = cursor.execute(sql,(userJSON['username'],userJSON['email'],userJSON['role'],hashed))
            dbConn.commit()
            count = cursor.rowcount
            return count
        finally:
            dbConn.close()

    @classmethod
    def deleteUser(cls,userid):
        dbConn = DatabasePool.getConnection()
        cursor = dbConn.cursor(dictionary=True)
        sql = "delete from user where userid = %s"
        users = cursor.execute(sql,(userid,))
        dbConn.commit()
        rows = cursor.rowcount
        dbConn.close()        
        return rows
    
    @classmethod
    def loginUser(cls,email,password):
        try:
            dbConn = DatabasePool.getConnection()
            cursor = dbConn.cursor(dictionary=True)
            password = password.encode('utf8')
            hashed = bcrypt.hashpw(password,bcrypt.gensalt())
            sql = 'select * from user where email=%s'
            cursor.execute(sql,(email,))
            user = cursor.fetchone()
            print(hashed)
            print(user['password'].encode())
            if (bcrypt.checkpw(user['password'].encode(),hashed)):
                payload={'userid':user['userid'],'role':user['role'],'exp':datetime.datetime.utcnow()+datetime.timedelta(seconds=3600)}
                token=jwt.encode(payload,Settings.secret,algorithm="HS256")
                return token
            else:
                return "wrong password"
        finally:
            dbConn.close()
