
import zmq
import os
import time
import sys
import glob
import ntpath

##============================================================================##
##------------------------------- sub.py -------------------------------------##
##============================================================================##
'''
Purpose:              ZMQ SUB working with queue as source of data for transfer

Author:               Yuliana Zamora
Email:                yzamora@uchicago.edu
Date Created:         June July 3, 2017
Date Last Modified:   July 5, 2017
'''

##============================================================================##
##-------------------------------- SUB() -------------------------------------##
##============================================================================##
def sub():
    print("In sub script")
    context = zmq.Context()
    subscriber = context.socket(zmq.SUB)
    #subscriber.connect("tcp://127.0.0.1:10111")
    subscriber.connect("tcp://127.0.0.1:10111")
    subscriber.setsockopt(zmq.SUBSCRIBE, b'')


    ####CREATING HANDSHAKE sequence############
    #synchronize with publisher
    syncclient = context.socket(zmq.REQ)
    syncclient.connect('tcp://127.0.0.1:10112')
    #msg = subscriber.recv(313344)
    #send a synchronization request
    syncclient.send('This is a message from subscriber')
    #wait for synchronization reply
    syncclient.recv()
    ###############################################

    print("About to receive")

    #def main():
    #while True:
    #/home/parallels/stream_transfer/test_files/test1.txt

    #files = glob.glob('/home/parallels/stream_transfer/test_files/*')
    #files = glob.glob('/tmp/ramdisk/*')
    #filename = 'test1.txt'

    #for filename in files:
    while True:
        destfile = '/home/parallels/stream_transfer/destination/'

        msg = subscriber.recv_multipart()
        #[fname,data] = msg.split()
        #filestrs = fname.split('/')
        #fn = destfile+filestrs[len(filestrs)-1]
        fn = destfile+"test.1"
        #f = open(fn, 'ab')
        with open(fn,'a') as f:
            print 'open'
            f.write(msg[1])
            print 'close\n'
        syncclient.send("Finished writing")
        syncclient.recv()
        break
        #f.close()


    ####CREATING HANDSHAKE sequence############
    #synchronize with publisher
    #syncclient = context.socket(zmq.REQ)
    #syncclient.connect('tcp://127.0.0.1:10113')
    #msg = subscriber.recv(313344)
    #send a synchronization request
    #syncclient.send('received all the data')
    #wait for synchronization reply
    #syncclient.send('F')
    ###############################################

########MAIN##########

if __name__ == '__main__':

    """context = zmq.Context()
    subscriber = context.socket(zmq.SUB)
    #subscriber.connect("tcp://127.0.0.1:10111")
    subscriber.connect("tcp://127.0.0.1:10111")
    subscriber.setsockopt(zmq.SUBSCRIBE, b'')"""
    while True:
       sub()
