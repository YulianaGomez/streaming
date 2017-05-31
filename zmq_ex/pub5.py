import zmq
import time
import os
import sys
import glob

####WORKING VERSION - can transfer streaming data, will no delete data from
####source after transfer
##def main():
context = zmq.Context()
publisher = context.socket(zmq.PUB)
publisher.bind("tcp://127.0.0.1:10111")
time.sleep(5)

print("About the send")

while True:

    print 'loop'
#msg = 'C:\TEMP\personnel.db'

# Prepare context & publisher


    files = glob.glob('/home/parallels/stream_transfer/test_files/*')
    #curFile = '/home/parallels/stream_transfer/test_files/test1.txt'
    for curFile in files:
        size = os.stat(curFile).st_size
    #print 'File size:',size

    target = open(curFile, 'rb')
    file = target.read(size)
    #if file:
    publisher.send(file)


    target.close()
    #time.sleep(10)

publisher.close()
context.term()
########MAIN##########

"""if __name__ == '_main__':

    while True:
        files = glob.glob('/home/parallels/stream_transfer/test_files/*')
        if len(files) > 0: main()
    else: time.sleep(1)"""
