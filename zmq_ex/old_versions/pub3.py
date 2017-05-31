import zmq
import time
import os
import sys
import glob

####NOT WORKING VERSION - trying to stream data###
SUBSCRIBERS_EXPECTED = 1
#while True:
#print 'loop'
#msg = 'C:\TEMP\personnel.db'
# Prepare context & publisher
context = zmq.Context()
print 'in context'
#socket to talk to clients
publisher = context.socket(zmq.PUB)
print 'in conxt.socket'
publisher.sndhwm = 11000
print 'debug'
publisher.bind("tcp://127.0.0.1:10111")
print 'debug2'
#publisher.bind('tcp://*:10111')
time.sleep(1)
print 'debug1'
#socket to receive signals ---order is request 
syncservice = context.socket(zmq.REP)
syncservice.bind('tcp://*:10112')
######MAKING SURE TO WAIT FOR SUBSCRIBER####
#subscribers = 0
#while subscribers < SUBSCRIBERS_EXPECTED:

    #print 'in second while loop'
    #wait for synchroniztion request
msg = syncservice.recv()
    #send synchronization reply
syncservice.send(b'')
#    subscriber += 1
#    print ("+1 subscriber (%i/%i)" % (subscriber,SUBSCRIBERS_EXPECTED))

files = glob.glob('/home/parallels/stream_transfer/test_files/*')
#print 'out of second while loop'
#curFile = 'C:/TEMP/personnel.db'
for curFile in files:
    size = os.stat(curFile).st_size
    #print 'File size:',size

    target = open(curFile, 'rb')
    file = target.read(size)
    #if file:
    publisher.send(file)
    target.close()

publisher.close()
context.term()


    #time.sleep(10)
