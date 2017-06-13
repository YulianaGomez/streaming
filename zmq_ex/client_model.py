"""CLIENT waiting for msg, sending requests ahead as credits,

Author: Yuliana Zamora
Email: yzamora@uchicago.edu
Last worked on: June 12, 2017
"""

import os
from threading import Thread

import zmq

from zhelpers import socket_set_hwm, zpipe

CHUNK_SIZE = 250

def client():
    ctx = zmq.Context()
    dealer = ctx.socket(zmq.DEALER)
    socket_set_hwm(dealer, 1)
    #dealer.connect("tcp://127.0.0.1:6000")
    dealer.connect("tcp://34.207.160.51:10120")
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
            #destroot = '/home/ubuntu/yzamora/streaming/destination/' #Rose's machine
            destroot = '/home/parallels/stream_transfer/destination/' #my machine 
            #chunk = dealer.recv()
            try:
                msg = dealer.recv_multipart()
            except zmq.ZMQError as e:
                if e.errno == zmq.ETERM:
                    return   # shutting down, quit
                else:
                    raise
            #print "msg = ",msg
            [fname, chunk] = msg

            filestrs = fname.split('/')
            fn = destroot+filestrs[len(filestrs)-1]

            #f = open(destfile, 'wb')
            #print 'Puting the chunk here:',fn
            f = open(fn, 'ab')
            #f = open(destfile, 'ab') #appends to the file, writes the entire file
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
        #if size < CHUNK_SIZE:
        #    break   # Last chunk received; exit

    print ("%i chunks received, %i bytes" % (chunks, total))
    #pipe.send(b"OK")



###################MAIN METHOD##########################

def main():

    # Start child threads
    #ctx = zmq.Context()
    #b = zpipe(ctx)

    #client = Thread(target=client_thread, args=(ctx, b))
    #server = Thread(target=server_thread, args=(ctx,))
    client()#.start()
    #server.start()

    # loop until client tells us it's done
    #try:
    #    print "sending data"
    #except KeyboardInterrupt:
    #    pass
    #del b
    #ctx.term()

if __name__ == '__main__':
    main()
