import pandas as pd
import utm
import pymongo
# check reading from xlsx
stations = pd.read_excel('./Tzrifin.xlsx')
lon= stations["Longitude"]
lat = stations["Latitude"]
#check the convertion to decimal degree
# print(utm.to_latlon(lon[1], lat[1], 36, 'U'))

# list for the data
list_siteID = []
list_lat =[]
list_lon = []
# remove multiple data in that columns
print(stations.columns)
for _ in stations[stations.columns[0]]:
    if _ not in list_siteID:
        list_siteID.append(_)
for _ in stations[stations.columns[2]]:
    if _ not in list_lat:
        list_lat.append(_)
for _ in stations[stations.columns[3]]:
    if _ not in list_lon:
        list_lon.append(_)
l = 197

list_antenna = []
list_all = []
for k in range(len(list_siteID)):
    antennas =[]
    for i in range(0,l):
        if list_siteID[k] == stations[stations.columns[0]][i]:
            for j in range(4,13):
                list_antenna.append(stations[stations.columns[j]][i])
        if list_antenna: 
            antennas.append(list_antenna)
        list_antenna = []
    list_station = []
    list_station.append(list_siteID[k])
    list_station.append(list_lat[k])
    list_station.append(list_lon[k])
    list_station.append(antennas)
    list_all.append(list_station)

print(list_all[0])

for _ in list_all:
    tup = utm.to_latlon(_[2], _[1], 36, 'U')
    _[1] = tup[0]
    _[2] = tup[1]
print(list_all[0])
# make all to dictionary
#put it all to the mongo db.
print(stations.columns)
print(stations.columns[0])
print(len(stations.columns))
print(len(list_all[0][3]))
myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["stations"]
mycol = mydb["stationi"]

my_all = {}
for _ in list_all:
    mydict = {}
    mydict[stations.columns[0]] = _[0]
    mydict[stations.columns[3]] = _[1]
    mydict[stations.columns[2]] = _[2]
    d ={}
    for an in _[3]:
        dict = {}
        dict[stations.columns[0]] = _[0]
        for i in range(0,9):
            dict[stations.columns[i+4]] = an[i]
        d[str(an[0])] = dict
        
    mydict["antennas"] = d
    my_all[_[0]] = mydict



dict1 = {}
for _ in my_all:
    for i in my_all[_]:
        if i != "antennas":
            dict1[i] = my_all[_][i]
    if not mycol.find(dict1):
        x = mycol.insert_one(dict1)
    dict1 = {}
dict2 = {}

mycol1 = mydb["antennas"] 
 
for _ in my_all:
    for i in my_all[_]:
        if i == "antennas":
            for t in my_all[_][i]:
                for j in my_all[_][i][t]:
                    dict2[j] = str(my_all[_][i][t][j])
                if not mycol1.find({"Site ID": dict2["Site ID"]}):
                    x = mycol1.insert_one(dict2)
                dict2 = {}



