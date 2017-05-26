
import zmq
import os
import time
import sys
import glob

while True:

    files = glob.glob('/home/parallels/globus-sdk-python/globusnram/test_files/*')
    path = '/home/parallels/globus-sdk-python/globusnram/test_files/'
    for filename in files:
        #filename = 'personnel.db'
        destfile = filename

        if os.path.isfile(destfile):
            os.remove(destfile)
            time.sleep(2)

        context = zmq.Context()
        subscriber = context.socket(zmq.SUB)
        subscriber.connect("tcp://127.0.0.1:2002")
        subscriber.setsockopt(zmq.SUBSCRIBE,'')

        msg = subscriber.recv(313344)
        if msg:
            f = open(destfile, 'wb')
            print 'open'
            f.write(msg)
            print 'close\n'
            f.close()

        time.sleep(5)
