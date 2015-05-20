# FinalBusSimulator
REST program for Bus simulation in python using Flask 

We have tried to model working of public transport, in Restful way using Python. We are using
Flask framework in order to achieve the same.
We are capturing following interactions between the different objects as observed in daily life.
• Bus knows beforehand about all the stops it has to make
• Passengers inform the stops that they have arrived and waiting for bus.
• The bus stop would let all the passengers waiting on the stop know that the bus has
arrived
• Bus conductor starts the bus from bus-depot and makes the first stop.
• Conductor let's all passengers board the bus after receiving correct amount.
• Conductor validates the amount received with respect to payment method, amount being
paid and age of the passenger.
• If the passenger is paying by cash and is senior citizen he would pay $3, if an adult then
he would pay $5 and if a child he would pay $2.
• Every time before the next stop arrives, bus broadcasts the name of the bus-stop.
• If a passenger wants to get down, he needs to inform the conductor.

For running the processes in order to see the interaction

1. Bus.py
python bus.py 3000 60

2. Conductor.py
python conductor.py

3. stop.py (run same code for different arguments to create many busstops)
python stop.py 5000 stop1
python stop.py 5002 stop2
python stop.py 5003 stop3

4. Passengers.py (run same code for different arguments to create many passengers)
python Passenger.py 7001 p1 5000 5002 Cash 5 7002 adult False
python Passenger.py 7002 p2 5000 5003 Cash 3 7001 senior True
python Passenger.py 7003 p3 5001 5002 Clipper 0 -1 adult False
python Passenger.py 7004 p4 5002 5004 studentId 0 7005 adult False
python Passenger.py 7005 p5 5003 5004 Clipper 0 7004 adult False
python Passenger.py 7006 p6 5003 5004 Cash 2 -1 child False
python Passenger.py 7007 p7 5001 5002 studentId 0 -1 adult False
python Passenger.py 7008 p8 5000 5001 Cash 8 -1 adult False


Demo video link:
https://youtu.be/oxscEWn5PFA
