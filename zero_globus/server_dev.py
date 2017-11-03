"""SERVER,
Server thread waits for a chunk request from a client,
reads that chunk and sends it back to the client

Author: Yuliana Zamora
Email: yzamora@uchicago.edu
Last worked on: June 14, 2017
"""
import os
import sys
import time
import glob
from threading import Thread
import time

import zmq

from zhelpers import socket_set_hwm, zpipe

#CHUNK_SIZE = 250

def server(router, files):
    #file = open(fn, "r")
    #t0 = time.time()
    #router = ctx.socket(zmq.ROUTER)

    """####Creating FIRST handshake sequence#######
    syncservice = context.socket(zmq.REP)
    syncservice.bind('tcp://*:10112')
    msg = syncservice.recv()
    print "Received request: ", msg
    syncservice.send("Message from server") #send synchronization reply
    ######################################
    print "past first handshake"""

    #router.bind("tcp://*:6000")

    """Creating handshake sequence
    syncservice = ctx.socket(zmq.REP)
    syncservice.bind('tcp://*:10112')
    msg = syncservice.recv()
    print "Received request: ", msg
    syncservice.send("Message from 10111")"""

    #while True: #removed to test non-streaming transfers
    # First frame in each message is the sender identity
    # Second frame is "fetch" command
    #files = glob.glob('/home/parallels/globus-sdk-python/globusnram/test_files/*')
    #files = glob.glob('/home/ubuntu/yzamora/streaming/test_files/*')
    for curFile in files:
        try:
            msg = router.recv_multipart()
        except zmq.ZMQError as e:
            if e.errno == zmq.ETERM:
               print "at error"
               return   # shutting down, quit
            else:
               raise
        [identity, command, chunksz_str] = msg
        if command != "fetch":
            print("Failed file metadata exchange!")
            sys.exit(1)

        chunksz = int(chunksz_str)
     	#cfile = open(curFile, "r")
        cfile =open("/dev/zero", "rb", 0)

        outer.send_multipart([identity, "/dev/null", "ready"])

        """print("File=" + str(curFile) + "; Chunk size=" + chunksz_str)"""
        while True:
            """
            msg = router.recv_multipart()
            identity, status, curr_offset_str = msg
            if status!="transfer":
                print("no transfer msg received.")
                sys.exit(3)"""
            #print("File=" + curFile + "; Client's offset=" + curr_offset_str)

	    # Read chunk of data from file
            #offset = int(curr_offset_str)
	    #cfile.seek(offset, os.SEEK_SET)
	    data = cfile.read(chunksz)

	    # Send resulting chunk to client
	    router.send_multipart([identity, data])

	    #deleting after file sent
	    #sys.getsizeof returns size in bytes,
	    #if data < chunk size, than there is
	    #nothing more toread after this

            if data=='':
               os.remove(curFile)
               break

    #########Creating second handshake sequence################

    """#print 'Finished sending data, waiting for second handshake'
    syncservice = context.socket(zmq.REP)

    #print 'waiting for handshake'
    syncservice.bind('tcp://*:10113')

    #print '...still waiting for handshake'
    msg = syncservice.recv() ##currently not getting past here

    #print "Received request: ", msg
    syncservice.send("Finished sending")
    #print "past sent part" """
    #t1 = time.time()
    #total = t1-t0
    #print ("total time to transfer: %f seconds"%total)
    ############################################################

    #target.close()
    #publisher.close()
    #print"past close and context terminate"


###################MAIN METHOD##########################

if __name__ == '__main__':
    # initialize zmq
    context = zmq.Context()
    router = context.socket(zmq.ROUTER)
    router.bind("tcp://*:10120")

    while True:
        #files = glob.glob('/home/ubuntu/yzamora/stream2/test_files/*')
        files = glob.glob('/home/yzamora/streaming/test_files/*')
        if len(files) > 0:
            t0 = time.time()
            server(router, files)
            break #use if testing for timing
        else:
            time.sleep(1)


###################CHECKING##############################
    try:
        msg = router.recv_multipart()
    except zmq.ZMQError as e:
        if e.errno == zmq.ETERM:
            print "at error"
            sys.exit(1)   # shutting down, quit
        else:
            raise
    [identity, command, chunksz_str] = msg
    if command != "fetch":
        print("Failed file metadata exchange!")
        sys.exit(1)
#############MSG SENT FROM CLIENT THAT IT RECEIVED FILE#######
    t1 = time.time()
    total = t1-t0
    print ("total time to transfer: %f seconds"%total)

    # finalize zmq
    router.close()
    context.term()
