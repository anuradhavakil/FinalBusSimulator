#!flask/bin/python
from flask import Flask, jsonify, abort, make_response, request
import sys
import json
import requests
import urllib2

app = Flask(__name__)

stopList = [];
@app.route('/Stop/api/v1.0/RegisterMe', methods=['POST'])
def registerMe():
    port =request.json.get('port',"")
    stopList.append(port);
    print 'Passenger with port number ' + str(port) + ' is waiting at my stop'
    print stopList;
    a= "You are registered! with port number"+ str(port)
    return a
    
@app.route('/Stop/api/v1.0/tellStop', methods=['POST'])
def tellPassenger():
    for i in stopList:
        
        starting = 'http://localhost:'+str(i)+'/Passanger/api/v1.0/BusArrived'
        headers = {'Content-Type': 'application/json'}
        data={'stop':i}
        r = requests.post(starting, data=json.dumps(data), headers=headers)
        print('Passengers Notified')
    return "Passengers Notified"



@app.route('/')
def index():
    print 'Hello I am', str(sys.argv)
    
    
if __name__ == '__main__':
    port=int(sys.argv[1])
    stopName=str(sys.argv[2])
    
    
    
    headers = {'Content-Type': 'application/json'}
    data={'port_number':port,'name':stopName}
    r = requests.post("http://localhost:3000/Bus/api/v1.0/RegisterStop", data=json.dumps(data), headers=headers)
    print('I have registered with the bus! It will now stop here')
    app.run(debug=True,port=port,use_reloader=False)
    
    