from flask import Flask, jsonify, Response, request, make_response
import pymongo
from bson import json_util
import json
import math


app = Flask(__name__, )

###########################
try:
    client = pymongo.MongoClient("mongodb+srv://Shimon37:Shimon37@cluster0.jcpog7i.mongodb.net/test")
    db = client["stations"]
    collection = db["antennai"]
except:
    print("ERROR - Cennot connect to DB")


def calculateCellId(id):
    endoeb = id//256
    # print(endoeb)
    if endoeb%10 == 0:
        endoeb //=10
    return endoeb # TODO implement


@app.route("/get_stations", methods=['POST'])
def get_station():
    try:
        global cell_tower_list
        mobile_cell_towers = request.get_json()
        mobile_cell_towers = list(mobile_cell_towers)
        # mobile_cell_towers = requestBody #json.loads(requestBody)
        # id = 0
        
        cell_info = list()
        private_tower = mobile_cell_towers[0]
        print(private_tower["rsrp"])
        enodeB = str(calculateCellId(int(private_tower["id"])))
        ###
        enodeB = 6037
        Pc_i = [370,98,291,329,159]
        ###
        siteID = collection.find({},{"Site ID":1,"_id":0})
        siteID = list(siteID)
        siteId = []
        for _ in siteID:
            siteId.append(_["Site ID"])
        privateSiteId = "IIIII"
        for _ in siteId:
            if str(enodeB) in _:
                privateSiteId = _ 
        # print(privateSiteId)
        pci = private_tower["pci"]
        query = {"$and": [{"Site ID": privateSiteId}, {"PCI": str(pci)}]}
        private_tower_info = collection.find(query,
                                 {"_id": 0, "Site ID": 1, "Latitude": 1, "Longitude": 1, "freq": 1, "Height (m)": 1,
                                  "Azimuth": 1, "PCI": 1, "Power (dBm)": 1})
        # print(private_tower_info)

        for tower in private_tower_info:
            tower_dict = dict()
            # print(tower)
            tower_dict["Site ID"] = tower["Site ID"]
            tower_dict["Latitude"] = tower["Latitude"]
            tower_dict["Longitude"] = tower["Longitude"]
            tower_dict["freq"] = tower["freq"]
            tower_dict["Height (m)"] = tower["Height (m)"]
            tower_dict["Azimuth"] = tower["Azimuth"]
            tower_dict["PCI"] = tower["PCI"]
            tower_dict["Power (dBm)"] = tower["Power (dBm)"]
            tower_dict["rsrp"] = private_tower["rsrp"]
            cell_info.append(tower_dict)
            # print(tower_dict)
            # print(tower["Site ID"])

        # mobile_cell_towers = list(mobile_cell_towers)
        cell_tower_list = mobile_cell_towers
        mobile_cell_towers.pop(0)
        # print(mobile_cell_towers)
        # print("mobile_cell_towers")
        # print(mobile_cell_towers)
        for cell_tower in mobile_cell_towers:
            # print(cell_tower["pci"])
            query = {"PCI": str(cell_tower["pci"])}
            towers = collection.find(query, {"_id": 0, "Site ID":1, "Latitude":1,"Longitude":1,"freq":1,"Height (m)":1,"Azimuth":1,"PCI":1,"Power (dBm)":1})
            # print(list(towers))
            for tower in towers:
                tower_dict = dict()
                tower_dict["Site ID"] = tower["Site ID"]
                tower_dict["Latitude"] = tower["Latitude"]
                tower_dict["Longitude"] = tower["Longitude"]
                tower_dict["freq"] = tower["freq"]
                tower_dict["Height (m)"] = tower["Height (m)"]
                tower_dict["Azimuth"] = tower["Azimuth"]
                tower_dict["PCI"] = tower["PCI"]
                tower_dict["Power (dBm)"] = tower["Power (dBm)"]
                # for i in mobile_cell_towers:
                tower_dict["rsrp"] = cell_tower["rsrp"]
                cell_info.append(tower_dict)
                # print(tower["Site ID"])

        cell_tower_list = list(cell_info)

        json_cell_info = json.dumps(cell_info)
        listStationsByDis ={}
        listStationsByDis[cell_tower_list[0]["Site ID"]] =0
        for _ in cell_tower_list:
            if _["Site ID"] != cell_tower_list[0]["Site ID"]:
                x0,y0 = cell_tower_list[0]["Latitude"], cell_tower_list[0]["Longitude"]
                x1,y1 = _["Latitude"] , _["Longitude"]
                p0 = [float(x0),float(y0)]
                p1 = [float(x1),float(y1)]
                listStationsByDis[_["Site ID"]] = math.dist(p0,p1)
            
        return json_cell_info
    except Exception as ex:
        return Response(response=json.dumps({"message": "sorry cannot update user"}), status=500,
                        mimetype="application/json")

def ericson(freq,hb,p,rsrp):
    hr=1.5 #m
    a0=36.2
    a1=30.2
    a2=12
    a3=0.1
    g=44.49*math.log(freq,10)-4.78*((math.log(freq,10))**2)
    delta = -18.12#db
    L=p-(10*math.log((12*100),10))-rsrp+delta #dB
    mekadem = (a1+a3*math.log(hb,10))
    eq =  a0+a2*math.log(hb,10)-(3.2*((math.log(11.75*hr)**2)))+g
    resualt = (L-eq)/mekadem
    r=((10.0**resualt))*1000
    # print(r)
    return(r)
@app.route("/get_location", methods=['GET'])
def get_location():
    try:
        listStationsByDis ={}
        listStationsByDis[cell_tower_list[0]["Site ID"]] =0
        for _ in cell_tower_list:
        # print(cell_tower_list)
            print(_)
        for _ in cell_tower_list:
            if _["Site ID"] != cell_tower_list[0]["Site ID"]:
                x0,y0 = cell_tower_list[0]["Latitude"], cell_tower_list[0]["Longitude"]
                x1,y1 = _["Latitude"] , _["Longitude"]
                p0 = [float(x0),float(y0)]
                p1 = [float(x1),float(y1)]
                listStationsByDis[_["Site ID"]] = math.dist(p0,p1)
        json_cell_info = json.dumps(cell_tower_list)
        sortedDis = sorted(listStationsByDis.items(),key=lambda x:x[1])

        print(sortedDis)
        r0,r1,r2 = 0,0,0
        for _ in cell_tower_list:
            if sortedDis[0][0] == _["Site ID"]:
                r0 = ericson(float(_["freq"]),float(_["Height (m)"]),float(_["Power (dBm)"]),_["rsrp"])
            if sortedDis[1][0] == _["Site ID"]:
                r1 = ericson(float(_["freq"]),float(_["Height (m)"]),float(_["Power (dBm)"]),_["rsrp"])
            if sortedDis[2][0] == _["Site ID"]:
                r2 = ericson(float(_["freq"]),float(_["Height (m)"]),float(_["Power (dBm)"]),_["rsrp"])
        print(r0,r1,r2)


        return json_cell_info
    except Exception as ex:
        print(ex)
        return Response(response=json.dumps({"message": "sorry cannot update user"}), status=500,
                        mimetype="application/json")
    
###########################
if (__name__ == "__main__"):
    app.run(host='0.0.0.0', port=5000, debug=True)
    # get_station()


