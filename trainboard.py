import http.client
import json
from datetime import datetime
import ssl #had issue with desktop and ssl certification expired
ssl._create_default_https_context = ssl._create_unverified_context

headers = {
    'python-Liveboard': 'python-Liveboard 1.0',
    'contact': 'joren.liegeois@gmail.com'  # This is another valid field
}

def getList():
    con = http.client.HTTPSConnection("api.irail.be")
    con.request("GET", "/liveboard/?station=Antwerp-Central&arrdep=departure&format=json", headers=headers)
    resp = con.getresponse()
    print("status of server request: ", resp.status)
    resp = resp.read()
    #print(resp) #for testing
    respList = json.loads(resp)
    #print(respList) #for testing
    departureList = respList["departures"]["departure"]
    return(departureList)

if __name__ == "__main__":
    departureList = getList()
    for x in departureList:
        print(x["station"], datetime.fromtimestamp(int(x["time"])).strftime('%H:%M:%S'), datetime.fromtimestamp(int(x["delay"])).strftime("%M"),  x["platform"], x["vehicleinfo"]["shortname"])
        #dest, time, platform, train name
