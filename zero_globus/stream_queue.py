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
import globus_transfer
import client_model
import streamonefile
import split_stream
import config
import create_queue
import pub_queue
import sub_queue


##============================================================================##
##------------------------------- stream_queue.py ----------------------------##
##============================================================================##
'''
Purpose:              Common app for ZMQ and Globus. User can choose how many
                      to create or if they want streaming data into one file.

Author:               Yuliana Zamora
Email:                yzamora@uchicago.edu
Date Created:         June 30, 2017
Date Last Modified:   July 2, 2017
'''

##============================================================================##
##-------------------------------- mult_files() ------------------------------##
##============================================================================##


#Creating multiple files. If file_number set to 0, create infinite files
def mult_files(file_number):
	filename = "filename_test"
	source_path      = "/home/parallels/stream_transfer/zero_globus/test_files/"
	#dest_path        = "/tmp/ramdisk/"
	max_iterations   = file_number

	#if   len(sys.argv) == 1: filename = filename_default
	#elif len(sys.argv) == 2: filename = sys.argv[1]
	#else:
	#    print "Syntax: python stream_onefile.py <FILE-optional>"
	#    sys.exit(1)

	iter = 0
	while True:
	    random_num = int(random.random()*1000000000)
	    #fname_src = source_path+filename+"."+str(random_num)
	    #fname_dst = dest_path+filename+"."+str(random_num)
	    fname_src = source_path+filename+"."+str(iter)
	    #fname_dst = dest_path+filename+"."+str(iter)
	    with open(fname_src,"wa") as f: f.write(str(iter)+"\n")
	    #subprocess.call(["mv",fname_src,fname_dst])
	    iter += 1
            if (file_number != 0):
	        if iter == max_iterations:
	            print "Max Iteration Reached. Done."; break

##============================================================================##
##-------------------------------- one_file() --------------------------------##
##============================================================================##
#Creating one file with multiple lines. If nlines =0, infinite lines
def one_file():
	# Input:
    filename = "filename_test"
    source_path      = "/home/parallels/stream_transfer/zero_globus/test_files2/"
    #dest_path        = "/Users/yzamora/streaming/zero_globus/destination/"
    nfiles           = 1
    nlines           = 0 #if zero infinite lines

    for ifile in xrange(nfiles):
            fname_src = source_path+filename+"."+str(ifile)
            #fname_dst = dest_path+filename+"."+str(ifile)
            with open(fname_src,"wr+") as f:
                iline = 0
                while True:
                    f.write("Adding line "+str(iline)+" in "+filename+"."+str(ifile)+"\n")
                    iline += 1
                    if (nlines <> 0) and (iline == nlines): break
    #subprocess.call(["mv",fname_src,fname_dst])
    print "All files Done."

##============================================================================##
##-------------------------------- stream_child() ----------------------------##
##============================================================================##
#Calls mult_file in a child thread
def stream_child():
    #file_number = input("How many files would you like to create? Enter 0 for infinite: ")
    if (file_number == 0): print ("Creating a streaming set of files. Ctrl+Z or C to stop")
    try:
        pid = os.fork()
        if pid == 0:
            #Chilff thread calls function
            mult_files(file_number)
            os._exit(0)
        else:
            if file_number ==0: time.sleep(1)
            #will exit so parent thread can work
            else: os.waitpid(pid,0)
            return
    except OSError, e:
        print >>sys.stderr, "fork failed: %d (%s)" % (e.errno, e.strerror)
        sys.exit(1)



################################################################################
##============================================================================##
##------------------------------------ MAIN ----------------------------------##
##============================================================================##
################################################################################

if __name__ == "__main__":

    #Parse Input
    #Flags corresponding to different inputs and configurations
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--globus", dest="globus", action = "store_true", default=False)
    parser.add_argument("-s", "--server", dest="server", action = "store_true", default=False)
    parser.add_argument("-c", "--client", dest="client", action = "store_true", default=False)
    parser.add_argument("-q", "--useq", dest="useq", action = "store_true", default=False)

    #parser.add_argument("-m", "--many", dest="many")
    #parser.add_argument("-o", "--one", dest="one")
    #parser.add_argument("-d" , "--dest_endpoint" , dest="dest_endpoint")
    #parser.add_argument("-s" , "--source_endpoint" , dest="source_endpoint")
    args = parser.parse_args()
    server = args.server
    globus = args.globus
    client = args.client
    useq = args.useq

    #If -c chosen, client side of ZMQ will run
    ##============================================================================##
    ##------------------------------ ZMQ CLIENT-----------------------------------##
    ##============================================================================##
    if client:
        print "You are running the client side with ZeroMQ. Waiting for server to send msgs."
        client_model.client(1024,"/home/parallels/stream_transfer/zero_globus/destination","34.207.160.51","10120")
    ##============================================================================##
    ##-------------------------------Random BYTES---------------------------------##
    ##============================================================================##
    elif globus and useq:
        print("You are running GLOBUS with a queue")
        pid = os.fork()
        if pid == 0:
            create_queue.qcreate()
            os.exit(0)
        pid2 = os.fork()
        if pid2 == 0:
            create_queue.put_infile()
            os.exit(0)
        while True:
            files = glob.glob('/home/parallels/stream_transfer/zero_globus/test_files/*')
            if len(files) > 0: globus_transfer.transfer(files)

    ##============================================================================##
    ##-------------------------------ZMQ with QUEUE-------------------------------##
    ##============================================================================##
    elif server and useq:
        print("You are running ZMQ server/pub side with a queue")
        t1 = threading.Thread(target=create_queue.qcreate())
        t1.start()
        print "Out of create_queue loop"
        q = MyConfig().q
        #print q.get()
        time.sleep(2)
        pub_queue.transfer()
    elif client and useq:
        print("You are running ZMQ client/sub side with a queue")
        sub_queue.sub()
    ##============================================================================##
    ##-------------------------------GLOBUS---------------------------------------##
    ##============================================================================##
    #If -g chosen, globus will run with corresponding other options
    elif globus:
        files = glob.glob('/home/parallels/stream_transfer/zero_globus/test_files/*')
        globus_transfer.service()
        print "You are running Globus"
        streaming_ans = raw_input("Would you like a file with streaming data?(yes or no): ")
        #User inputs yes/no depending on whether they want streaming data within in a file
        if (streaming_ans == 'yes') or (streaming_ans == 'y'):
            print "Streaming data into file is being created."
            #Streaming of data in one file is created in a different directory
            file2 = glob.glob('/home/parallels/stream_transfer/zero_globus/test_files2/*')
            pid = os.fork()
            if pid == 0:
                streamonefile.manage_split()
                os._exit(0)
            #Files from test_files2 will be split up and put in test_files directory
            pid2 = os.fork()

            #Splitting file created into specificied chunks
            if pid2 == 0:
                split_stream.split_file(file2)
                os._exit(0)
            while True:
                files = glob.glob('/home/parallels/stream_transfer/zero_globus/test_files/*')
                if len(files) > 0: globus_transfer.transfer(files)

        #User can input 0 for streaming files and int for specific number
        else:
            file_number = input("How many files would you like to be created?(0 for infinite): ")
            if (file_number == 0): print ("Creating a streaming set of files. Ctrl+Z or C to stop")
            print("Files are being created in:/home/parallels/stream_transfer/zero_globus/test_files/ ")
            stream_child()
	    if len(files) > 0: globus_transfer.transfer()
    ##============================================================================##
    ##------------------------------ ZMQ SERVER------- ---------------------------##
    ##============================================================================##
    elif server:
        print "You are starting the server side with ZMQ"
        stream_child()
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
