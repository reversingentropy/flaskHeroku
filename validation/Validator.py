import functools,re
from flask import jsonify,request,Flask,g
from config.Settings import Settings
import jwt

def login_required(func):
        @functools.wraps(func)
        def checkLogin(*arg,**kwargs):
            auth=True
            auth_header = request.headers.get('Authorization') 
            if auth_header:
                auth_token = auth_header.split(" ")[1]
            else:
                auth_token = ''
                auth=False
            
            if auth_token:
                try:
                    payload = jwt.decode(auth_token,Settings.secret,algorithms=['HS256'])
                    g.userid = payload['userid']
                    g.role = payload['role']
                except Exception as err:
                    print(err)
                    auth=False
            
            if (auth==False):
                message = {"message":"Invalid or missing JWT"}
                return jsonify(message),403
            
            return func(*arg, **kwargs)

        return checkLogin

def require_admin(func):
        @functools.wraps(func)
        def checkRole(*arg,**kwargs):
            if g.role != "admin":
                message = {"message":"user is not an admin."}
                return jsonify(message),403           
            return func(*arg,**kwargs)

        return checkRole

def require_isAdminOrSelf(func):
    @functools.wraps(func)
    def checkAdminOrSelf(*args,**kwargs):
        if g.userid != kwargs['userid']:
            if g.role != "admin":
                message = {"message":"user is not an admin or intended user."}
                return jsonify(message),403
        return func(*args,**kwargs)
    return checkAdminOrSelf

def validateRegister(func):
    @functools.wraps(func)
    def validate(*args,**kwargs):
        username = request.json['username']
        email = request.json['email']
        role = request.json['role']
        password = request.json['password']
        print("username : ",username)
        print("email : ",email)
        print("role : ",role)
        print("password : ",password)
        patternUsername = re.compile('^[a-zA-Z0-9]+$')
        patternEmail = re.compile('^[a-zA-Z0-9]+[\.]?[a-zA-Z0-9]+@\w+\.\w+$')
        patternPassword = re.compile('^[a-zA-Z0-9]{8,}')
        print(patternUsername.match(username))
        print(patternEmail.match(email))
        print(patternPassword.match(password))
        if (patternUsername.match(username) and patternEmail.match(email) and patternPassword.match(password)):
            return func(*args,**kwargs)
        else:
            return jsonify({"message":"validation failed"}),403
        
    return validate