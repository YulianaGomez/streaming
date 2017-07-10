import zmq
import time
import os
import sys
import glob
import time

"""WORKING VERSION - correct version of pub4 s
has correct placement of context and terminations,
deletes files after being transferred, waits for new files to transfer
than delete. achieves timing of transfer

6/1/2017 - can transfer data (121M h5 files) from ramdisk to chosen
destination -2.389 seconds

Yuliana Zamora
yzamora@uchicago.edu
Last worked on: July 5, 2017
PURPOSE: Working with queue and multi"""

def transfer():
    #print("in tranfers loop")
    # Prepare context & publisher - must set up context first
    t0 = time.time()
    context = zmq.Context()
    publisher = context.socket(zmq.PUB)
    publisher.bind("tcp://127.0.0.1:10111")
    #time.sleep(5)

    """Creating handshake sequence"""
    syncservice = context.socket(zmq.REP)
    syncservice.bind('tcp://*:10112')
    msg = syncservice.recv()
    print "Received request: ", msg
    syncservice.send("Message from 10111") #send synchronization reply



    files = glob.glob('/home/parallels/stream_transfer/test_files/*')
    for f in files:
        print 'loop'
        size = os.stat(f).st_size
        #print 'File size:',size

        target = open(f, 'rb')
        ff = target.read(size) #number of bytes to read from file
        #if file:
        sendfile = f +' '+ ff
        item_pub = sendfile.split()
        item_name = item_pub[0]
        print 'name from pub side = ',item_name
        publisher.send("%s %s" % (f,ff))
        print 'sent msg from pub side'

    """Creating second handshake sequence"""

    #print 'Finished sending data, waiting for second handshake'
    syncservice = context.socket(zmq.REP)

    #print 'waiting for handshake'
    syncservice.bind('tcp://127.0.0.1:10113')

    #print '...still waiting for handshake'
    msg = syncservice.recv() ##currently not getting past here

    #print "Received request: ", msg
    syncservice.send("Finished sending")
    #print "past sent part"
    t1 = time.time()
    total = t1-t0
    print ("total time to transfer: %f seconds"%total)

    #target.close()
    publisher.close()
    context.term()
    #print"past close and context terminate"


            ########MAIN##########

if __name__ == '__main__':
    #t0 = time.time()
    transfer()
