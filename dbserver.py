# from flask import Flask
# from pymongo import MongoClient

# app = Flask(__name__)

# client = MongoClient('localhost', 27017)

# db = client.flask_db
# stations = db.stations

# @app.route("/get_file/<filename>")
# def get_file(filename):
#     return stations.send_file(filename)

# import pymongo

# myclient = pymongo.MongoClient("mongodb://localhost:27017/")
# mydb = myclient["stations"]
# mycol = mydb["stationi"]

# mydict = { "name": "John", "address": "Highway 37" }

# x = mycol.insert_one(mydict)

from flask import Flask , jsonify,Response,request,make_response
# import jwt
import datetime
import pymongo
import json
from bson.objectid import ObjectId
app = Flask(__name__)
# app.config['SECRET_KEY'] ='thisisthesecretkye'
###########################
try:
    mongo = pymongo.MongoClient(host="localhost",port=27017,serverSelectionTimeoutMS =1000)
    db =mongo.stations
    mongo.server_info()
except:
    print("ERROR - Cennot connect to DB")
###########################
@app.route("/users", methods=["POST"])
def create_user():
    try:
        mycol= db["users"]
        if mycol.find_one({"userName":request.form["userNAme"]}) == None:
            user = {"userName":request.form["userName"],"password":request.form["password"],"test":request.form["test"]}
            dbResponse = db.users.insert_one(user)
            return Response(response= json.dumps({"message":"user created","id":f"{dbResponse.inserted_id}"}),status=200,mimetype="application/json")            
        else:
            return Response(response= json.dumps({"message":"Username is taken"}),status=200,mimetype="application/json")
    except Exception as ex:
        print("**********")
        print(ex)
        print("**********")
###########################
@app.route("/users", methods=["GET"])
def get_some_users():
    try:
        data =list (db.users.find())
        for user in data:
            user["_id"] = str(user["_id"])
        return  Response(response= json.dumps(data),status=200,mimetype="application/json")
    except Exception as ex:
      print(ex)
      return Response (response= json.dumps({"message":"cannot read users"}),status=500,mimetype="application/json" )
###########################