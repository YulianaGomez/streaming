"""SERVER sending credits, waiting for messages,
Server thread waits for a chunk request from a client,
reads that chunk and sends it back to the client

Author: Yuliana Zamora
Email: yzamora@uchicago.edu
Last worked on: June 5, 2017
"""
import os
from threading import Thread

import zmq

from zhelpers import socket_set_hwm, zpipe

CHUNK_SIZE = 250

def server_thread(ctx):
    file = open("testdata", "r")

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

        identity, command, offset_str, chunksz_str = msg

        assert command == b"fetch"

        offset = int(offset_str)
        chunksz = int(chunksz_str)

        # Read chunk of data from file
        file.seek(offset, os.SEEK_SET)
        data = file.read(chunksz)

        # Send resulting chunk to client
        router.send_multipart([identity, data])


###################MAIN METHOD##########################

def main():
        # Start child threads
        ctx = zmq.Context()
        a = zpipe(ctx)

        #client = Thread(target=client_thread, args=(ctx, b))
        server = Thread(target=server_thread, args=(ctx,))
        #client.start()
        server.start()

        # loop until client tells us it's done
        try:
            print a.recv()
        except KeyboardInterrupt:
            pass
        del a
        ctx.term()

if __name__ == '__main__':
    main()
