#!/usr/bin/env python

import os
import sys
import random
import subprocess
import time
import glob
import argparse
import zmq
from Queue import Queue
import threading

from config import MyConfig
#import globus_transfer
import client_model
import streamonefile
import split_stream
import config
import create_queue
import pub_queue
import sub_queue
import var_stream


##============================================================================##
##------------------------------- stream_queue.py ----------------------------##
##============================================================================##
'''
Purpose:              ZMQ script manager. Scripts to run with streaming files,
                      streaming queue, streaming bytes into file

Author:               Yuliana Zamora
Email:                yzamora@uchicago.edu
Date Created:         July 10, 2017
Date Last Modified:   July 10, 2017
'''
def zmq_manager(client,server,useq):
 #If -c chosen, client side of ZMQ will run
##============================================================================##
##-------------------------------ZMQ with QUEUE-------------------------------##
##============================================================================##
    if server and useq:
        print("You are running ZMQ server/pub side with a queue")
        #t1 = threading.Thread(target=create_queue.qcreate())
        #t1.start()
        #create_queue.qcreate()
        print "Out of create_queue loop"
        #q = MyConfig().q
        #print q.get()
        #time.sleep(2)
        pub_queue.transfer()
    elif client and useq:
        print("You are running ZMQ client/sub side with a queue")
        sub_queue.sub()
    #If -c chosen, client side of ZMQ will run
##============================================================================##
##------------------------------ ZMQ CLIENT-----------------------------------##
##============================================================================##
    elif client:
        print "You are running the client side with ZeroMQ. Waiting for server to send msgs."
        client_model.client(1024,"/home/parallels/stream_transfer/zero_globus/destination/","34.207.160.51","10120")
##============================================================================##
##------------------------------ ZMQ SERVER------- ---------------------------##
##============================================================================##
    elif server:
        print "You are starting the server side with ZMQ"
        var_stream.stream_child()
        print "Your files are being created and will be sent to client/sub via ZMQ once connected"
        context = zmq.Context()
        router = context.socket(zmq.ROUTER)
        router.bind("tcp://*:10120")

        while True:
            #files = glob.glob('/home/ubuntu/yzamora/stream2/test_files/*')
            files = glob.glob('/home/parallels/stream_transfer/zero_globus/test_files/*')
            if len(files) > 0:
                t0 = time.time()
                server_new.server(router, files)
                break #use if testing for timing
            else:
                time.sleep(1)
    else:
        print "You haven't picked a message passage interface: -c or -s for client/server usage in zeromq or -g for globus"
