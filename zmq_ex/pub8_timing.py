import zmq
import time
import os
import sys
import glob
import time

"""WORKING VERSION - correct version of pub4 s
has correct placement of context and terminations,
deletes files after being transferred, waits for new files to transfer
than delete. achieves timing of transfer

Yuliana Zamora
yzamora@uchicago.edu
Last worked on: June 1, 2017
TO DO:
Must figure out the handshake sequence"""

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

    ##while True: #removed to get none streaming transfer done
    # Read files (names) from fs
    files = glob.glob('/home/parallels/stream_transfer/test_files/*')
    #if len(files) > 0:
    #    print("About the send")
    for f in files:
        print 'loop'
        size = os.stat(f).st_size
        #print 'File size:',size

        target = open(f, 'rb')
        ff = target.read(size)
        #if file:
        publisher.send(ff)
        os.remove(f)
        #print('Finished removing files from source directory')
        #target.close()
        #time.sleep(10)
        #print('Target closed')

    #publisher.close()
    #context.term()
        """Creating second handshake sequence"""

    print 'Finished sending data, waiting for second handshake'
    syncservice = context.socket(zmq.REP)

    print 'waiting for handshake'
    syncservice.bind('tcp://127.0.0.1:10113')

    print '...still waiting for handshake'
    msg = syncservice.recv() ##currently not getting past here

    print "Received request: ", msg
    syncservice.send("Finished sending")
    print "past sent part"
    t1 = time.time()
    total = t1-t0
    print ("total time to transfer: %f seconds"%total)

    #target.close()
    publisher.close()
    context.term()
    print"past close and context terminate"


            ########MAIN##########

if __name__ == '__main__':
    t0 = time.time()
    transfer()
    t1 = time.time()
    total = t1-t0
    #print ("total time to transfer: %f seconds"%total)
    #while True:
    #    files = glob.glob('/home/parallels/stream_transfer/test_files/*')

    #    if len(files) > 0: transfer()
            #t0 = time.time()
            #transfer()
            #t1 = time.time()
            #total = t1-t0 #send a publisher end msg to subscriber, subscriber
            #sends request message using socket,publish waits for reply socket,
            #subcribe received file using req rep sockets
            #print ("Total time of transfer: %f seconds"%total)

    #else:
    #    time.sleep(1)
    #    print("in else")

    #publisher.close()
    #context.term()
