#!flask/bin/python
from flask import Flask, jsonify, abort, make_response, request
import urllib2
import urllib
import time
import sys
import thread
import threading
import requests
import json

from flask_httpauth import HTTPBasicAuth



app = Flask(__name__)
auth = HTTPBasicAuth()

communication_Conductor =[{'Message':'Acknowledged.'}]

@auth.get_password
def get_password(username):
    if username == 'project2':
        return 'Rest'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error':'Access Denied'}),401)

conductor =[
        {'id': 1,
         'port_number': '0000'
        }
        ]
busstop =[
        
        ]

passengers =[
        
        ]




    
@app.route('/Bus/api/v1.0/registerConductor', methods=['POST'])
@auth.login_required
def conductor_reg():
    if not request.json or not 'port_number' in request.json:
        abort(400)
        
    task={
           'id':conductor[-1]['id']+1,
           'port_number':request.json.get('port_number',"")
        }
    conductor.append(task)
    print 'I now have a conductor!'
    return "Request acknowledeged",201


@app.route('/Bus/api/v1.0/EnterBus', methods=['POST'])
def passengerEnter():
    if not request.json or not 'port' in request.json:
        abort(400)
        
    task={
           'port':request.json.get('port',"")
        }
    passengers.append(task)
    print 'Passenger Aboard!!'
    return "Request acknowledeged",201


def passengerExit():
    if not request.json or not 'port' in request.json:
        abort(400)
        
    
    
    print 'Passenger exited!!'
    return "Request acknowledged",201


@app.route('/Bus/api/v1.0/initializeBus', methods=['GET'])
def bus_initialize():
    
    return "Bus started,201"    

busPort=int(sys.argv[1])
start_bus_timer = int(sys.argv[2])

def main():
    thread = threading.Thread(target=run)
    thread.daemon = True                           
    thread.start()   

def run():
    print 'Bus will start after '+ str(start_bus_timer) +' seconds'
    time.sleep(float(start_bus_timer))
    print 'Time for bus departure, requesting conductor to start bus..'
    if (start_bus()!= True):
        print 'Bus broken....:('
        
    for b in busstop:
        time.sleep(float(60))
        print 'Stop' + b.get('name') + 'approaching.. Stop Bus'
        if (stop_bus()!= True):
            print 'Bus broken....:('
        print "Passengers : Bus stop number " + str(b.get('port_number')) + " is approaching! Please get ready to exit"
        informPassengers(b.get('port_number'))
        print "All passengers have now exited. New Passengers may board!"
        if (inform_stop(b.get('port_number'))!= True):
            print 'Bus broken....:('
        print 'Requesting conductor to start bus..'
        if (start_bus()!= True):
            print 'Bus broken....:('
            
    print 'Bus Journey Ended. Returning to Depot'
    if (stop_bus()!= True):
            print 'Bus broken....:('
        
       
def informPassengers(portNumber):
    
    
    for p in passengers:
        try:
            url = 'http://localhost:'+ str(p.get('port')) + '/Passanger/api/v1.0/StopArrived'
            data = {"port":portNumber}
            headers = {'Content-Type': 'application/json'}
            r = requests.post(url, data=json.dumps(data), headers=headers)
           
        except urllib2.HTTPError, e:
            print "HTTP error: %d" % e.code
            
        except urllib2.URLError, e:
            print "Network error: %s" % e.reason.args[1]
            
    
    
           
        
        
        
    
def start_bus():
    try:
        data = urllib2.urlopen('http://localhost:3001/conductor/api/v1.0/conductor/busStarted').read()
    except urllib2.HTTPError, e:
        print "HTTP error: %d" % e.code
        return False
    except urllib2.URLError, e:
        print "Network error: %s" % e.reason.args[1]
        return False
    print data
    return True
    
    
    
def inform_stop(port_number):
    try:
        url = 'http://localhost:'+ str(port_number) + '/Stop/api/v1.0/tellStop'
        data = {"message":"Bus Arrived"}
        headers = {'Content-Type': 'application/json'}
        r = requests.post(url, data=json.dumps(data), headers=headers)
        print "Passengers Aboard! Doors closing"
        return True
    except urllib2.HTTPError, e:
        print "HTTP error: %d" % e.code
        return False
    except urllib2.URLError, e:
        print "Network error: %s" % e.reason.args[1]
        return False
    
    
def stop_bus():
    try:
        data = urllib2.urlopen('http://localhost:3001/conductor/api/v1.0/conductor/busStopped').read()
    except urllib2.HTTPError, e:
        print "HTTP error: %d" % e.code
        return False
    except urllib2.URLError, e:
        print "Network error: %s" % e.reason.args[1]
        return False
    print data
    return True
    

@app.route('/Bus/api/v1.0/RegisterStop', methods=['POST'])
def busstop_reg():
    if not request.json or not 'port_number' in request.json:
        abort(400)
        
    task={
           
           'port_number':request.json.get('port_number',""),
           'name':request.json.get('name',"")
        }
    busstop.append(task)
    
    print 'I need to stop at ' + request.json.get('name',"")
    
    return "Request acknowledeged",201

    

if __name__ == '__main__':
    '''
    time.sleep(float(start_bus_timer))
    '''
    main()
    app.run(debug=True,port=3000,use_reloader=False)