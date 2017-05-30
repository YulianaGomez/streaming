import zmq
import time
import os
import sys
import glob

##def main():
while True:

    print 'loop'
#msg = 'C:\TEMP\personnel.db'

# Prepare context & publisher
    context = zmq.Context()
    publisher = context.socket(zmq.PUB)
    publisher.bind("tcp://127.0.0.1:10111")
    time.sleep(1)

    #files = glob.glob('/home/parallels/stream_transfer/test_files/*')
    curFile = '/home/parallels/stream_transfer/test_files/test1.txt'
    #for curFile in files:
    size = os.stat(curFile).st_size
    #print 'File size:',size

    target = open(curFile, 'rb')
    file = target.read(size)
    #if file:
    publisher.send(file)

    publisher.close()
    context.term()
    target.close()
    time.sleep(10)


########MAIN##########

##if __name__ == '_main__':
##    main()
