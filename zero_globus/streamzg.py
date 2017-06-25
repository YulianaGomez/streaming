#!/usr/bin/env python

import os
import sys
import random
import subprocess
import time
import glob
import argparse
import zmq

import globus_transfer
import client_model
import server_new

##============================================================================##
##------------------------------- stream_data.py -----------------------------##
##============================================================================##
'''
Purpose:              Countinuously creates random new files.

Author:               Yuliana Zamora
Email:
Date Created:         June 22, 2017
Date Last Modified:   June 24, 2017
'''

################################################################################
##============================================================================##
##------------------------------------ MAIN ----------------------------------##
##============================================================================##
################################################################################

# Input:

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



def one_file():
	# Input:
	filename_default = "filename_test"
	source_path      = "/home/ubuntu/yzamora/streaming/"
	dest_path        = "/home/ubuntu/yzamora/streaming/test_files/"
	nfiles           = 1
	nlines           = 1000000

	if   len(sys.argv) == 1: filename = filename_default
	elif len(sys.argv) == 2: filename = sys.argv[1]
	else:
	    print "Syntax: python stream_onefile.py <FILE-optional>"
	    sys.exit(1)

	for ifile in xrange(nfiles):
	    fname_src = source_path+filename+"."+str(ifile)
	    fname_dst = dest_path+filename+"."+str(ifile)
	    with open(fname_src,"wa") as f:
	        for iline in xrange(nlines):
	            f.write("Adding line "+str(iline)+" in "+filename+"."+str(ifile)+"\n")
	    subprocess.call(["mv",fname_src,fname_dst])
	print "All files Done."

def stream_child():
    file_number = input("How many files would you like to create? Enter 0 for infinite: ")
    if (file_number == 0): print ("Creating a streaming set of files. Ctrl+Z or C to stop")
    try:
        pid = os.fork()
        if pid == 0: 
            mult_files(file_number)
            os._exit(0)
        else:     
            if file_number ==0: time.sleep(1)
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

	parser = argparse.ArgumentParser()
	parser.add_argument("-g", "--globus", dest="globus", action = "store_true", default=False)
	parser.add_argument("-s", "--server", dest="server", action = "store_true", default=False)
	parser.add_argument("-c", "--client", dest="client", action = "store_true", default=False)
	#parser.add_argument("-m", "--many", dest="many")
	#parser.add_argument("-o", "--one", dest="one")
	#parser.add_argument("-d" , "--dest_endpoint" , dest="dest_endpoint")
	#parser.add_argument("-s" , "--source_endpoint" , dest="source_endpoint")
	args = parser.parse_args()
	server = args.server
	globus = args.globus
        client = args.client

	if client:
	    print "You are running the client side with ZeroMQ. Waiting for server to send msgs."
	    client_model.client(1024,"/home/parallels/stream_transfer/zero_globus/destination","34.207.160.51","10120")

	elif globus:
            globus_transfer.service()
            print "You are running Globus"
            file_number = input("How many files would you like to create? Enter 0 for infinite: ")
            if (file_number == 0): print ("Creating a streaming set of files. Ctrl+Z or C to stop")
            try:
                pid = os.fork()
                if pid == 0:
                    mult_files(file_number)
                    os._exit(0)
                else:
                    if file_number ==0: time.sleep(1)
            except OSError, e:
                print >>sys.stderr, "fork failed: %d (%s)" % (e.errno, e.strerror)
                sys.exit(1)
            

            files = glob.glob('/home/parallels/stream_transfer/zero_globus/test_files/*')
    	    if len(files) > 0: 
                globus_transfer.transfer()
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
