
import zmq
import zmq.ssh
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
Date Created:         June 3, 2017
Date Last Modified:   December 20, 2017
'''

##============================================================================##
##-------------------------------- SUB() -------------------------------------##
##============================================================================##
global_stop = False
context = zmq.Context()
syncclient = context.socket(zmq.REQ)
#syncclient.connect('tcp://127.0.0.1:10112')
zmq.ssh.tunnel_connection(syncclient, "tcp://127.0.0.1:10111", "cc@129.114.33.7")
def sub():
    print global_stop
    #print("In sub script")
    #context = zmq.Context()
    subscriber = context.socket(zmq.SUB)
    #subscriber.connect("tcp://127.0.0.1:10111")
    #subscriber.connect("tcp://127.0.0.1:10112")
    zmq.ssh.tunnel_connection(subscriber, "tcp://127.0.0.1:10112", "cc@129.114.33.7")
    #subscriber.setsockopt(zmq.SUBSCRIBE, b'')
    subscriber.setsockopt(zmq.SUBSCRIBE, '')


    ####CREATING HANDSHAKE sequence############
    #synchronize with publisher
    #msg = subscriber.recv(313344)
    #send a synchronization request
    syncclient.send('This is a message from subscriber')
    #wait for synchronization reply
    syncclient.recv()
    ###############################################

    print("About to receive")
    bsend=1000000000
    bsent=0
    chunk=1000
    with open('/dev/null','wb') as f:
        while bsent < bsend:
            msg = subscriber.recv()
            #print('recieving')
            f.write(msg[1])
            f.flush()
            bsent+=chunk

########MAIN##########

if __name__ == '__main__':

    """context = zmq.Context()
    subscriber = context.socket(zmq.SUB)
    #subscriber.connect("tcp://127.0.0.1:10111")
    subscriber.connect("tcp://127.0.0.1:10111")
    subscriber.setsockopt(zmq.SUBSCRIBE, b'')"""
    while True:
       sub()

