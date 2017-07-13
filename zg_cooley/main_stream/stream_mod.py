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
import config
import create_queue
import pub_queue
import sub_queue
import zmq_manager




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

##============================================================================##
##------------------------------ ZMQ Manager-----------------------------------##
##============================================================================##
    if client or server:
        zmq_manager.zmq_manager(client,server,useq)
    else: print("Hello")
