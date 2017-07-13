
import zmq
import os
import time
import sys
import glob
import ntpath
import threading

##============================================================================##
##------------------------------- sub.py -------------------------------------##
##============================================================================##
'''
Purpose:              ZMQ SUB working with queue as source of data for transfer

Author:               Yuliana Zamora
Email:                yzamora@uchicago.edu
Date Created:         June July 3, 2017
Date Last Modified:   July 6, 2017
'''

##============================================================================##
##-------------------------------- SUB() -------------------------------------##
##============================================================================##
global_stop = False
context = zmq.Context()
syncclient = context.socket(zmq.REQ)
syncclient.connect('tcp://127.0.0.1:10112')
def sub():
    print global_stop
    #print("In sub script")
    context = zmq.Context()
    subscriber = context.socket(zmq.SUB)
    #subscriber.connect("tcp://127.0.0.1:10111")
    subscriber.connect("tcp://127.0.0.1:10111")
    subscriber.setsockopt(zmq.SUBSCRIBE, b'')


    ####CREATING HANDSHAKE sequence############
    #synchronize with publisher
    #syncclient = context.socket(zmq.REQ)
    #syncclient.connect('tcp://127.0.0.1:10112')
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
    destfile = '/home/parallels/stream_transfer/zero_globus/destination'
    fn = destfile+"test.1"
    t1 = threading.Thread(target=listen)
    t1.start()
    with open(fn,'a') as f:
        while not global_stop:
            msg = subscriber.recv_multipart()
            #[fname,data] = msg.split()
            #filestrs = fname.split('/')
            #fn = destfile+filestrs[len(filestrs)-1]

            #f = open(fn, 'ab')
            print 'open'
            f.write(msg[1])
            f.flush()
            print 'close'
            #time.sleep(1)

        print "done?"




        #break
        #f.close()

def listen():
    syncclient.send("Still listening")
    syncclient.recv()
    #print "got a msg"
    syncclient.send("Finished writing")
    #time.sleep(2)
    print "setting exit"
    global_stop = True
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
