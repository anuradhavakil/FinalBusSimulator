#!flask/bin/python
from flask import Flask, jsonify, abort, make_response, request
import requests
import json
import urllib2


app = Flask(__name__)


payment =[
        {'id': 1,
         'title': u'Clipper',
         'description': u'Paid by Clipper',
         'done': False
        },
        {'id': 2,
         'title': u'Cash',
         'description': u'Paid by Cash',
         'done': False
        },
        {'id': 3,
         'title': u'Student Id',
         'description': u'Showed valid Student Id',
         'done': False
        }
        ]
communication_Passenger =[{'Message':'Hello, you need to pay first.'}]



@app.route('/Conductor/api/v1.0/conductor', methods=['GET'])
def get_tasks():
    r = jsonify({'communication_Passenger':communication_Passenger})
    return r

@app.route('/Conductor/api/v1.0/ValidatePayment', methods=['POST'])
def validate_payment():
    if not request.json or not 'paymentType' in request.json or not 'paymentNumber' in request.json:
        abort(400)
    print " In conductor payment"
    a=request.json.get('paymentType',"")
    b=request.json.get('paymentNumber',"")
    print 'Passanger has paid using ', a, 'and his payment number is ',b 
    return 'Success'




def main():
    
    try:
        url = 'http://project2:Rest@localhost:3000/Bus/api/v1.0/registerConductor'
        data = {"port_number":"3003"}
        headers = {'Content-Type': 'application/json'}

        r = requests.post(url, data=json.dumps(data), headers=headers)
    
        print "Conductor successfully registered,201"
    except urllib2.HTTPError, e:
        print "HTTP error: %d" % e.code
    except urllib2.URLError, e:
        print "Network error: %s" % e.reason.args[1]

@app.route('/conductor/api/v1.0/conductor/busStarted', methods=['GET'])
def bus_started():
    print "I am now starting the bus"
    return "Bus started,201"         

@app.route('/conductor/api/v1.0/conductor/busStopped', methods=['GET'])
def bus_stopped():
    print "I am now stopping the bus"
    return "Bus stopped,201"  

if __name__ == '__main__':
    main()
    app.run(debug=True,port=3001,use_reloader = False)