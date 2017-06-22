#!/usr/bin/env python

import os
import sys
import random
import subprocess
import time
import glob
import argparse

##============================================================================##
##------------------------------- stream_data.py -----------------------------##
##============================================================================##
'''
Purpose:              Countinuously creates random new files.

Author:               Yuliana Zamora
Email:
Date Created:         June 22, 2017
Date Last Modified:   June 22, 2017
'''

################################################################################
##============================================================================##
##------------------------------------ MAIN ----------------------------------##
##============================================================================##
################################################################################

# Input:

def mult_files():
	filename_default = "filename_test"
	source_path      = "/home/parallels/stream_transfer/"
	dest_path        = "/tmp/ramdisk/"
	max_iterations   = 1000

	if   len(sys.argv) == 1: filename = filename_default
	elif len(sys.argv) == 2: filename = sys.argv[1]
	else:
	    print "Syntax: python stream_onefile.py <FILE-optional>"
	    sys.exit(1)

	iter = 0
	while True:
	    random_num = int(random.random()*1000000000)
	    #fname_src = source_path+filename+"."+str(random_num)
	    #fname_dst = dest_path+filename+"."+str(random_num)
	    fname_src = source_path+filename+"."+str(iter)
	    fname_dst = dest_path+filename+"."+str(iter)
	    with open(fname_src,"wa") as f: f.write(str(iter)+"\n")
	    subprocess.call(["mv",fname_src,fname_dst])
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
	parser.add_argument("-z", "--zeromq", dest="zeromq", action = "store_true", default=False)
	parser.add_argument("-g", "--globus", dest="globus", action = "store_true", default=False)
	#parser.add_argument("-d" , "--dest_endpoint" , dest="dest_endpoint")
	#parser.add_argument("-s" , "--source_endpoint" , dest="source_endpoint")
	args = parser.parse_args()
	globus = args.globus
	zeromq = args.zeromq

	if zeromq:
	    print "You are running with zeromq"
	else:
		if globus:
			print "You are running globus"
		else:
			print "wrong"