from flask import Flask , jsonify,Response,request,make_response
# import jwt
import datetime
import pymongo
import json
from bson.objectid import ObjectId
app = Flask(__name__)
###########################
try:
    mongo = pymongo.MongoClient(host="localhost",port=27017,serverSelectionTimeoutMS =1000)
    db =mongo.stations
    mongo.server_info()
except:
    print("ERROR - Cennot connect to DB")
###########################

@app.route("/stations")
def create_station():
    # mycol= db["stationss"]
    try:
        user = {"station_id":12345678,"password":"12345678","test":"12345678"}
        dbResponse = db.stationss.insert_one(user)
        return Response(response= json.dumps({"message":"user created"}),status=200,mimetype="application/json") 
    except Exception as ex:
        print("**********")
        print(ex)
        print("**********")

###########################
@app.route("/stationid/<id>")
def get_station(id):
    try:
        print(id)
        # print(db)
        user_db=db.stationi.find_one({"Site ID": id})
        # user_json = json.dumps(user_db)
        user_db1=db.antennas.find({"Site ID": id})
        # print(type(user_json))
        # print("*****************")
        print(user_db)
        for _ in user_db1:
            print(_)
        if user_db is not None:
            
            return Response(response= json.dumps({"message":"Username is taken"}),status=200,mimetype="application/json")
        else:
            return Response(response= json.dumps({"message":"Username"}),status=200,mimetype="application/json")
    except Exception as ex:
        print("*****************")
        print(ex)
        print("*****************")
        return Response(response= json.dumps({"message":"sorry cannot update user"}),status=500,mimetype="application/json")
###########################
if __name__ == '__main__':
    app.run(debug=True)


