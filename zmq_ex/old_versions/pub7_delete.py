import zmq
import time
import os
import sys
import glob

"""WORKING VERSION - correct version of pub4 s
has correct placement of context and terminations,
deletes files after being transferred - works with sub6_delete and sub5"""

def transfer():
    print("in tranfers loop")
    # Prepare context & publisher
    context = zmq.Context()
    publisher = context.socket(zmq.PUB)
    publisher.bind("tcp://127.0.0.1:10111")
    time.sleep(5)


    # Read files (names) from fs
    files = glob.glob('/home/parallels/stream_transfer/test_files/*')

    print("About the send")
    for f in files:
        print 'loop'
        size = os.stat(f).st_size
        #print 'File size:',size

        target = open(f, 'rb')
        ff = target.read(size)
        #if file:
        publisher.send(ff)
        os.remove(f)

        target.close()
        #time.sleep(10)

    publisher.close()
    context.term()

    print 'Waiting for more data'
    ########MAIN##########

if __name__ == '__main__':

    while True:
        files = glob.glob('/home/parallels/stream_transfer/test_files/*')
        if len(files) > 0: transfer()
    else: time.sleep(1)
