
import zmq
import os
import time
import sys
import glob
import ntpath

"""WORKING VERSION - can accept streaming data from pub4.py
has correct placement of context and terminations, can delete data after
transfer is complete, waits for more data once transfer is complete
works with pub5,6,7,8 versions

6/1/2017 - can accept data from ramdisk

Yuliana Zamora
email: yzamora@uchicago.edu
Last worked on: June 1, 2017

"""
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

files = glob.glob('/home/parallels/stream_transfer/test_files/*')
#files = glob.glob('/tmp/ramdisk/*')
#filename = 'test1.txt'

for filename in files:
    print "In for loop"
    destfile = '/home/parallels/stream_transfer/destination/'

    msg = subscriber.recv()
    #if msg:
    [fname,data] = msg.split()
    filestrs = fname.split('/')
    fn = destfile+filestrs[len(filestrs)-1]
    f = open(fn, 'wb')
    print 'open'
    f.write(data)
    print 'close\n'
    f.close()


####CREATING HANDSHAKE sequence############
#synchronize with publisher
syncclient = context.socket(zmq.REQ)
syncclient.connect('tcp://127.0.0.1:10113')
#msg = subscriber.recv(313344)
#send a synchronization request
syncclient.send('received all the data')
#wait for synchronization reply
syncclient.recv()
###############################################

########MAIN##########
"""
if __name__ == '_main__':
    while True:
        main()"""
