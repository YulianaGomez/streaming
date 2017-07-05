import zmq
import time
import os
import sys
import glob
import time
import create_queue
from config import MyConfig
import Queue


##============================================================================##
##------------------------------- pub_q2.py ----------------------------------##
##============================================================================##
'''
Purpose:              ZMQ PUB working with queue as source of data for transfer

Author:               Yuliana Zamora
Email:                yzamora@uchicago.edu
Date Created:         June July 3, 2017
Date Last Modified:   July 5, 2017
'''

##============================================================================##
##-------------------------------- Transfer() --------------------------------##
##============================================================================##

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
    q = MyConfig().q
    #--------------------CREATING QUEUE TO TRANSFER----------------------------#
    zq = Queue.Queue()
    for rn in xrange(15):
        zq.put(rn)


    #files = glob.glob('/home/parallels/stream_transfer/test_files/*')
    #for f in files:
    #--------------------------INITIATE ZMQ PUB--------------------------------#
    print ("Initiating zmq transfer")
    #print q.get()
    #size = os.stat(f).st_size
    #print 'File size:',size
    #target = open(f, 'rb')
    #ff = target.read(size) #number of bytes to read from file
    f = "/home/parallels/stream_transfer/test_files/queue.ex"
    #sendfile = f +' '+ ff
    #item_pub = sendfile.split()
    #item_name = item_pub[0]
    #print 'name from pub side = ',item_name
    while not zq.empty():
    #print q.get()
        #print zq.get()
    #for r in xrange(10):
        v = zq.get()
        #print q.get()
        publisher.send_multipart((str(f),str(v)))
        print "sent msg from pub side"

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
