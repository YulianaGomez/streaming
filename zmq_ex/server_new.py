"""SERVER sending credits, waiting for messages,
Server thread waits for a chunk request from a client,
reads that chunk and sends it back to the client

Author: Yuliana Zamora
Email: yzamora@uchicago.edu
Last worked on: June 13, 2017
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

def server():


    #file = open(fn, "r")
    to = time.time()
    context = zmq.Context()
    router = context.socket(zmq.ROUTER)
    #router = ctx.socket(zmq.ROUTER)

    ####Creating FIRST handshake sequence#######
    syncservice = context.socket(zmq.REP)
    syncservice.bind('tcp://*:10112')
    msg = syncservice.recv()
    print "Received request: ", msg
    syncservice.send("Message from 10111") #send synchronization reply
    ######################################

    #router.bind("tcp://*:6000")

    router.bind("tcp://*:10120")
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
    files = glob.glob('/home/ubuntu/yzamora/streaming/test_files/*')
    for curFile in files:
        cfile = open(curFile, "r")
        try:
            msg = router.recv_multipart()
        except zmq.ZMQError as e:
            if e.errno == zmq.ETERM:
	    print "at error"
                return   # shutting down, quit
            else:
                raise

        identity, command, offset_str, chunksz_str = msg #msg is a list
        #assert command == b"fetch"

        offset = int(offset_str)
        chunksz = int(chunksz_str)

        # Read chunk of data from file
        cfile.seek(offset, os.SEEK_SET)
        data = cfile.read(chunksz)

        # Send resulting chunk to client
        router.send_multipart([identity, curFile, data])

        #deleting after file sent
        if sys.getsizeof(data) < chunksz:
            #remove file after it is sent!
            os.remove(curFile)

    #########Creating second handshake sequence################

    #print 'Finished sending data, waiting for second handshake'
    syncservice = context.socket(zmq.REP)

    #print 'waiting for handshake'
    syncservice.bind('tcp://*:10113')

    #print '...still waiting for handshake'
    msg = syncservice.recv() ##currently not getting past here

    #print "Received request: ", msg
    syncservice.send("Finished sending")
    #print "past sent part"
    t1 = time.time()
    total = t1-t0
    print ("total time to transfer: %f seconds"%total)
    ############################################################

    #target.close()
    publisher.close()
    context.term()
    #print"past close and context terminate"



        """try:
            msg = router.recv_multipart()
        except zmq.ZMQError as e:
            if e.errno == zmq.ETERM:
                print "at error"
                return   # shutting down, quit
            else:
                raise"""

###################MAIN METHOD##########################

def main():
    server()
        # Start child threads
        #files = glob.glob('/home/parallels/stream_transfer/test_files/*')
        #for fn in files:
        #    ctx = zmq.Context()
        #    a = zpipe(ctx)

            #client = Thread(target=client_thread, args=(ctx, b))
        #    server = Thread(target=server_thread, args=(ctx,))
            #client.start()
        #    server.start()

            # loop until client tells us it's done
        #    try:
        #        print a.recv()
        #    except KeyboardInterrupt:
        #        pass
        #    del a
        #    ctx.term()

if __name__ == '__main__':
    while True:
        #files = glob.glob('/home/parallels/stream_transfer/test_files/*')
        files = glob.glob('/home/ubuntu/yzamora/streaming/test_files/*')
        if len(files) > 0:
            main()
        else:
            time.sleep(1)
