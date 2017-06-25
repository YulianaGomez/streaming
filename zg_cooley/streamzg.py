#!/usr/bin/env python

import os
import sys
import random
import subprocess
import time
import glob
import argparse
import zmq

#import globus_transfer
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
Date Last Modified:   June 23, 2017
'''

#i###############################################################################
##============================================================================##
##------------------------------------ MAIN ----------------------------------##
##============================================================================##
################################################################################

# Input:

def mult_files(numberfiles):
	filename = "filename_test"
	#source_path      = "/home/parallels/stream_transfer/"
	#dest_path        = "/tmp/ramdisk/"
	source_path      = "/home/yzamora/streaming/test_files/"
	dest_path        = "/home/yzamora/streaming/destination/"
	max_iterations   = numberfiles

	#if   len(sys.argv) == 1: filename = filename_default
	#elif len(sys.argv) == 2: filename = sys.argv[1]
	#else:
	    #print "Syntax: python stream_onefile.py <FILE-optional>"
	    #sys.exit(1)

	iter = 0
	while True:
	    random_num = int(random.random()*1000000000)
	    #fname_src = source_path+filename+"."+str(random_num)
	    #fname_dst = dest_path+filename+"."+str(random_num)
	    fname_src = source_path+filename+"."+str(iter)
	    fname_dst = dest_path+filename+"."+str(iter)
	    with open(fname_src,"wa") as f: f.write(str(iter)+"\n")
	    #subprocess.call(["mv",fname_src,fname_dst])
	    iter += 1
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


################################################################################
##============================================================================##
##------------------------------------ MAIN ----------------------------------##
##============================================================================##
################################################################################



if __name__ == "__main__":
#Parse Input   

	parser = argparse.ArgumentParser()
	parser.add_argument("-c", "--client", dest="client", action = "store_true", default=False)
	parser.add_argument("-g", "--globus", dest="globus", action = "store_true", default=False)
	parser.add_argument("-s", "--server", dest="server", action = "store_true", default=False )
	parser.add_argument("-m", "--many", dest="many")
	parser.add_argument("-o", "--one", dest="one")
	#parser.add_argument("-d" , "--dest_endpoint" , dest="dest_endpoint")
	#parser.add_argument("-s" , "--source_endpoint" , dest="source_endpoint")
	args = parser.parse_args()
	server = args.server
	globus = args.globus
	client = args.client

	if client:
	    print "You are running the client side with ZeroMQ. Waiting for server to send msgs."
	    client_model.client(1024,"/home/yzamora/streaming/zero_globus/","140.221.68.131","10120")

	elif globus:
	        globus_transfer.service()
		print "You are running Globus"
		files = glob.glob('/home/yzamora/streaming/test_files/*')
        	if len(files) > 0: 
		    globus_transfer.transfer()
	elif server:
	        print "You are starting the server side"
		user_request = int(input("How many files would you like to create? Enter 0 for infinite: "))
		mult_files(user_request)
		print "Your files are being created and will be sent to client/sub via ZMQ"
		context = zmq.Context()
                router = context.socket(zmq.ROUTER)
                router.bind("tcp://*:10120")

	        while True:
	        #files = glob.glob('/home/ubuntu/yzamora/stream2/test_files/*')
	            files = glob.glob('/home/yzamora/streaming/test_files/*')
	            if len(files) > 0:
	                t0 = time.time()
	            	server_new.server(router, files)
	            	break #use if testing for timing
	            else:
	            	time.sleep(1)


        else:
	    print "You haven't picked a message passage interface: -c or -s to use client/server in zeromq or -g for globus"
