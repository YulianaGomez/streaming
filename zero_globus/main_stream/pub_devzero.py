import zmq
import time
import os
import sys
import glob
import time
import create_queue
from config import MyConfig
import Queue
import threading


##============================================================================##
##------------------------------- pub_q2.py ----------------------------------##
##============================================================================##
'''
Purpose:              ZMQ PUB working with queue as source of data for transfer

Author:               Yuliana Zamora
Email:                yzamora@uchicago.edu
Date Created:         June 3, 2017
Date Last Modified:   December 20, 2017
'''

##============================================================================##
##-------------------------------- Transfer() --------------------------------##
##============================================================================##

def transfer():
    print("in tranfers script")
    # Prepare context & publisher - must set up context first
    #t0 = time.time()
    context = zmq.Context()
    publisher = context.socket(zmq.PUB)
    #publisher.bind("tcp://127.0.0.1:10112")
    publisher.bind("tcp://*:10112")
    #time.sleep(5)

    """Creating handshake sequence"""
    syncservice = context.socket(zmq.REP)
    syncservice.bind('tcp://*:10111')
    msg = syncservice.recv()
    print "Received request: ", msg
    syncservice.send("Message from 10111") #send synchronization reply


    
    time.sleep(3)
    t0 = time.time()


    bsend = 1000000000
    chunk = 1000
    bsent = 0

    with open('/dev/zero', 'rb', 0) as f:

        while bsent < bsend:

            bsent += chunk
            datachunk = f.read(chunk)
            print('sending'+datachunk)
            publisher.send(datachunk)
            #time.sleep(1)


    """Creating second handshake sequence"""
    """"
    #print 'Finished sending data, waiting for second handshake'
    syncservice = context.socket(zmq.REP)

    #print 'waiting for handshake'
    syncservice.bind('tcp://127.0.0.1:10113')

    #print '...still waiting for handshake'
    msg = syncservice.recv() ##currently not getting past here

    print "Received request: ", msg
    syncservice.recv()"""
    print("print finished")
    #print "past sent part""""
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
