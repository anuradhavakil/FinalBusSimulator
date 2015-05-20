#!flask/bin/python
from flask import Flask, jsonify, abort, make_response, request
import sys
import requests
import threading

import urllib2
import json
import time
import random


app = Flask(__name__)

communication_Passenger =[{'Message':'Thank you!'}]

SpeechArray=['Hey', 'Wassup','Hope everything is fine', 'Yeah', 'Hmm','It is a nice day today!']

@app.route('/Passanger/api/v1.0/BusArrived', methods=['POST'])
def bus_arrived():
    print "My bus arrived, need to communicate with conductor now for payment!"
    '''With conductor for payment'''
    headers = {'Content-Type': 'application/json'}
    data={'paymentType': paymentType, 'paymentNumber': paymentNumber,'age':age}
    r = requests.post("http://localhost:3001/Conductor/api/v1.0/ValidatePayment", data=json.dumps(data), headers=headers)
   
    ''' With Bus'''
    if r.text[:300]=="Success" :
        print 'Yay! My payment was successful! Entering Bus'
        data={'port': port}
        busReq = requests.post("http://localhost:3000/Bus/api/v1.0/EnterBus",data=json.dumps(data), headers=headers )
        print 'I am now in the Bus!'
        ''' With Stop'''
              
        return 'Thank you bus'        
    return 'Thank you conductor'


@app.route('/Passanger/api/v1.0/StopArrived', methods=['POST'])
def stop_arrived():
    if not request.json or not 'port' in request.json:
        abort(400)
    if str(request.json.get('port')) == str(endPoint):
        print "I am getting down! at " + str(request.json.get('port'))
        url = 'http://localhost:3000/Bus/api/v1.0/GettingDown'
        data = {"port":port}
        headers = {'Content-Type': 'application/json'}
        r = requests.post(url, data=json.dumps(data), headers=headers)
        print "Bye Bye Bus!"  
    return "Ok"

@app.route('/Passanger/api/v1.0/talk', methods=['POST'])
def talk():
    if not request.json or not 'Speech' in request.json:
        abort(400)
    print "Friend "+str(friend)+" said: "+ request.json.get('Speech',"")
    return "Hi I got what you said! It was "+ request.json.get('Speech',"")
    

@app.route('/')
def index():
    print 'Hello I am', str(sys.argv)
    return "Hello, I am Passanger!"

def Speak():
    
    while True :
        
        time.sleep(random.randrange(100,150))
        print "Feel like talking to my friend: "+str(friend)
        try:
            headers = {'Content-Type': 'application/json'}
            word=random.choice(SpeechArray)
            data={'Speech': word}
            print "Sending "+word+"..."
            url="http://localhost:"+str(friend)+"/Passanger/api/v1.0/talk"
            r = requests.post(url, data=json.dumps(data), headers=headers)
        except Exception, e:
            print "Looks like my friend is sleeping " 
        except urllib2.URLError, e:
            print "Looks like my friend is sleeping %s" % e.reason.args[1]
            
        
    
    
def talkToFriend():
    thread = threading.Thread(target=Speak)
    thread.daemon = True                            # Daemonize thread
    thread.start() 
    
    

if __name__ == '__main__':
    port=int(sys.argv[1])
    passangerName=str(sys.argv[2])
    startPoint=str(sys.argv[3])
    endPoint=str(sys.argv[4])
    paymentType=str(sys.argv[5])
    paymentNumber=int(sys.argv[6])
    friend=int(sys.argv[7])
    age=str(sys.argv[8])
    
    
    if paymentType=="Cash":
        if age=="Senior":
            paymentNumber=3
        if age=="Adult":
            paymentNumber=5
        if age=="Child":
            paymentNumber=2
            
    '''Register with stop first
    try:
        data = urllib2.urlopen('http://localhost:' +startPoint+ '/Stop/api/v1.0/RegisterMe').read()
    except urllib2.HTTPError, e:
        print "HTTP error: %d" % e.code
    except urllib2.URLError, e:
        print "Network error: %s" % e.reason.args[1]
    print 'Stop says' , data
    
    ''' 
    
    headers = {'Content-Type': 'application/json'}
    data={'port': port}
    r = requests.post('http://localhost:' +startPoint+ '/Stop/api/v1.0/RegisterMe', data=json.dumps(data), headers=headers)
    print(r.text[:300] + '...')
    
    if friend!= -1:
        talkToFriend()
    app.run(debug=True,port=port, use_reloader=False)
    
    