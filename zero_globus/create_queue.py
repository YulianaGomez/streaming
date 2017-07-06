from config import MyConfig
import threading
from Queue import Queue
import os
import sys
import random
import time

"""

Purpose:              Creating queueing system

Author:               Yuliana Zamora
Email:                yzamora@uchicago.edu
Date Created:         June 30, 2017
Date Last Modified:   June 30, 2017
"""
##============================================================================##
##-------------------------------QUEUE----------------------------------------##
##============================================================================##

#Create queue
def qcreate():
    print "Creating queueing system"
    #q = Queue(0)
    #print("Queue is being created")
    q = MyConfig().q
    print("In queue child thread")
    for rn in xrange(1000):
    #while True:
        #rn = random.random()
        q.put(rn)
        #print ("Put %i in queue", rn)
    print("Finished creating queue")
    #os._exit(0)



#Takes items from queue and puts in file of specific size
def put_infile():
    q = MyConfig().q
    #print q
    destination = "/home/parallels/stream_transfer/zero_globus/test_files/"
    requested_size = 10
    filnum = 0
    #print "this is third function:", q.get()

    #While there are files to create, create a file
    print("Creating file of specific size from queue")
    while not q.empty():
        print "While queue is not empty"
        curFile = destination+"filename" + '.' + str(filnum)
        with open(curFile,"wb") as f:
            while (os.path.getsize(curFile) <= requested_size):
                print "Writing into file"
                v = q.get()
                print v
                f.write(str(v))
                f.flush()
                #return
            #f.close()
        filnum += 1
    print "Outside of while loop"
    os._exit(0)

def runforglob():
    t1 = threading.Thread(target=qcreate)
    t2 = threading.Thread(target=put_infile)
    #t3 = threading.Thread(target=qget)
    t1.start()
    t2.start()
    #t3.start()

if __name__ == "__main__":
    runforglob()
