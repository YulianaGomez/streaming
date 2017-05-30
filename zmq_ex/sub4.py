
import zmq
import os
import time
import sys
import glob
import ntpath


#def main():
while True:
#/home/parallels/stream_transfer/test_files/test1.txt

    files = glob.glob('/home/parallels/stream_transfer/test_files/*')
    #path = '/home/parallels/stream_transfer/test_files/'
    #filename = 'test1.txt'
    for filename in files:
        destfilename = ntpath.basename(filename)
        #filename = 'personnel.db'
    #destfilename = 'test1.txt'
        destfile = '/home/parallels/stream_transfer/destination/' + destfilename

        if os.path.isfile(destfile):
            os.remove(destfile)
            #time.sleep(2)

        context = zmq.Context()
        subscriber = context.socket(zmq.SUB)
        subscriber.connect("tcp://127.0.0.1:10111")
        subscriber.setsockopt(zmq.SUBSCRIBE,'')

        #msg = subscriber.recv(313344)
        msg = subscriber.recv()
        #if msg:
        f = open(destfile, 'wb')
        print 'open'
        f.write(msg)
        print 'close\n'
        f.close()

        time.sleep(5)

########MAIN##########
"""
if __name__ == '_main__':
    while True:
        main()"""
