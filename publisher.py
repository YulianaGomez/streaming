import zmq
import time
import os
import sys
import glob


def transfer_zeromq():
    print 'Starting to "send" messages'
    #msg = '/home/parallels/globus-sdk-python/globusnram/test_files/new_test.txt'


    # Prepare context & publisher
    context = zmq.Context()
    publisher = context.socket(zmq.PUB)
    publisher.bind("tcp://*:10111")
    time.sleep(1)


    files = glob.glob('/home/parallels/globus-sdk-python/globusnram/test_files/*')
    for curFile in files:
#    curFile = '/home/parallels/globus-sdk-python/globusnram/test_files/f'

        size = os.stat(curFile).st_size
        print 'File size:',size

        target = open(curFile, 'rb')
        file = target.read(size)
        if file:
            publisher.send(file)
        #os.remove(curFile)
        publisher.close()
        context.term()
        target.close()
        time.sleep(10)

#=================================================================================#
#-------------------------------      MAIN      ----------------------------------#
#=================================================================================#

if __name__ == "__main__":

    while True:
        #my_file = Path("/home/parallels/globus-sdk-python/globusnram/test_files/")
        #if my_file.is_file():
        #    transfer()
        files = glob.glob('/home/parallels/globus-sdk-python/globusnram/test_files/*')
        if len(files) > 0: transfer_zeromq()
        else: time.sleep(1)
