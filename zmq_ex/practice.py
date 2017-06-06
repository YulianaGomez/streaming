# File Transfer model #3
#
# In which the client requests each chunk individually, using
# command pipelining to give us a credit-based flow control.

import os
import zmq
import time
import sys
import glob
import ntpath
from threading import Thread

import zmq

from zhelpers import socket_set_hwm, zpipe

CHUNK_SIZE = 250

#Client sends number of requests ahead, each time it processes an incoming chunk
def client_thread(ctx, pipe):
    dealer = ctx.socket(zmq.DEALER)
    socket_set_hwm(dealer, 1)
    dealer.connect("tcp://127.0.0.1:6000")

    total = 0       # Total bytes received
    chunks = 0      # Total chunks received

    while True:
        # ask for next chunk
        dealer.send_multipart([
            b"fetch",
            b"%i" % total,
            b"%i" % CHUNK_SIZE
        ])

        try:
            destfile = '/home/parallels/stream_transfer/zmq_ex/test_open.txt'
            chunk = dealer.recv()
            #f = open(destfile, 'wb')
            f = open(destfile, 'ab') #appends to the file, writes the entire file
            print 'open'
            f.write(chunk)
            print 'close\n'
            f.close()
        except zmq.ZMQError as e:
            if e.errno == zmq.ETERM:
                return   # shutting down, quit
            else:
                raise

        chunks += 1
        size = len(chunk)
        total += size
        if size < CHUNK_SIZE:
            break   # Last chunk received; exit

    print ("%i chunks received, %i bytes" % (chunks, total))
    pipe.send(b"OK")

# File server thread
# The server thread waits for a chunk request from a client,
# reads that chunk and sends it back to the client:

def server_thread(ctx,fn):

    file = open(fn, "r")

    router = ctx.socket(zmq.ROUTER)

    router.bind("tcp://*:6000")

    while True:
        # First frame in each message is the sender identity
        # Second frame is "fetch" command
        try:
            msg = router.recv_multipart()
        except zmq.ZMQError as e:
            if e.errno == zmq.ETERM:
                return   # shutting down, quit
            else:
                raise

        identity, command, offset_str, chunksz_str = msg #msg is a list
        #print "this is identity: ",offset_str
        assert command == b"fetch"

        offset = int(offset_str)
        chunksz = int(chunksz_str)

        # Read chunk of data from file
        file.seek(offset, os.SEEK_SET)
        data = file.read(chunksz)

        # Send resulting chunk to client
        router.send_multipart([identity, data])

        #remove file after it is sent!
        os.remove(fn)


# The main task is just the same as in the first model.

def main():

    # Start child threads
    #ctx = zmq.Context()
    #a,b = zpipe(ctx)
    #print "this is b: ",b
    files = glob.glob('/home/parallels/stream_transfer/test_files/*')
    for fn in files:
        #destfilename = ntpath.basename(fn)
        ctx = zmq.Context()
        a,b = zpipe(ctx)
        client = Thread(target=client_thread, args=(ctx, b))
        server = Thread(target=server_thread, args=(ctx,fn))
        client.start()
        server.start()

        # loop until client tells us it's done
        try:
            print a.recv()
        except KeyboardInterrupt:
            pass
        del a,b
        ctx.term()



###########MAIN FUNCTION#####################

if __name__ == '__main__':

    while True:
    #will loop as long as ther are files in the path
        files = glob.glob('/home/parallels/stream_transfer/test_files/*')
        if len(files) > 0:
            main()
        else:
            time.sleep(1)
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

#main()
