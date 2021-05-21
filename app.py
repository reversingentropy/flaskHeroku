from flask import Flask, jsonify,request
from model.User import User
from validation.Validator import *
import re
from flask_cors import CORS
import bcrypt

app = Flask(__name__)

@app.route('/')
def validate():
    password = b"12345678"
    hashed = bcrypt.hashpw(password,bcrypt.gensalt())
    print("hashed",hashed)
    print("salt",bcrypt.gensalt())
    result = "Didn't match"
    if bcrypt.checkpw(password,hashed):
        result="it matches"
    print(result)
    return result

@app.route('/users/<int:userid>')
def getUser(userid):
    results = User.getUser(userid)

    jsonUsers={"Users":results}
    
    return jsonify(jsonUsers),200

@app.route('/users')
@login_required
@require_admin
def getAllUsers():
    results = User.getAllUsers()
    jsonUsers = {'Users': results}
    return jsonify(jsonUsers),200

@app.route('/users',methods=['POST'])
@validateRegister
@login_required
def insertUsers():
    userJSON=request.json
    output = User.insertUser(userJSON)
    jsonOutput={"Rows Affected " : output}
    return jsonify(jsonOutput),201


@app.route('/users/<int:userid>',methods=['DELETE'])
@login_required
@require_isAdminOrSelf
def deleteUser(userid):
    userJSON = request.json
    output = User.deleteUser(userid)
    jsonOutput={"Rows Affected " : output}
    return jsonify(jsonOutput),201

@app.route('/category')
def getAllCategory():
    try:
        jsonCat=category.getAllCategory()
        jsonCat={"Category":jsonCat}
        return jsonify(jsonCat),200

    except Exception as err:
        print(err)
        return {},500

@app.route('/category/<int:catid>/furniture')
def getFurniturebyCat(catid):
    try:
        jsonFurn = furniture.getFurnitureByCat(catid)
        jsonFurn = {" Furniture":jsonFurn}
        return jsonify(jsonFurn),200

    except Exception as err:
        print(err)
        return {},500


@app.route('/users/login',methods=['POST'])
def login():
    try:
        jsonBody = request.json
        token = User.loginUser(jsonBody['email'],jsonBody['password'])
        message = {'jwt':token}
        return jsonify(message),200
        
    except Exception as err:
        print(err)
        return {},500


if __name__ == '__main__': 
    app.run(debug=True)
    