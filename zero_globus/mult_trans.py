import os
import sys
#from globus_sdk import (TransferClient, TransferAPIError, TransferData, DeleteData, AccessTokenAuthorizer)
import os.path
#import globus_sdk
import glob
from pathlib import Path
from os import makedirs
import gl_refresh_chameleon


def multi_transfer():
    one_endpoint = False #set to True when sending to one endpoint
    chameleon = True
    #ep_count = 0
    with open("endpoints.dat") as f:
      #ep = f.readlines()
      ep = [line.rstrip('\n') for line in f]

    #print 'ep',ep
    #sys.exit(0)

    if not chameleon:
        src0 = "/home/parallels/stream_transfer/zero_globus/test_files/bigfile_test.0"
        src1 = "/home/parallels/stream_transfer/zero_globus/test_files/bigfile_test.1"
        src2 = "/home/parallels/stream_transfer/zero_globus/test_files/bigfile_test.2"
        src3 = "/home/parallels/stream_transfer/zero_globus/test_files/bigfile_test.3"
        src4 = "/home/parallels/stream_transfer/zero_globus/test_files/bigfile_test.4"
        src5 = "/home/parallels/stream_transfer/zero_globus/test_files/bigfile_test.5"

        src_path_all = '/home/parallels/stream_transfer/zero_globus/test_files'
    else:
        src0 = "/home/cc/streaming/zero_globus/test_files/bigfile_test.0"
        src1 = "/home/cc/streaming/zero_globus/test_files/bigfile_test.1"
        src2 = "/home/cc/streaming/zero_globus/test_files/bigfile_test.2"
        src3 = "/home/cc/streaming/zero_globus/test_files/bigfile_test.3"
        src4 = "/home/cc/streaming/zero_globus/test_files/bigfile_test.4"
        src5 = "/home/cc/streaming/zero_globus/test_files/bigfile_test.5"

        src_path_all = '/home/cc/streaming/zero_globus/test_files'


    """src0 = "/home/parallels/stream_transfer/zero_globus/test_files"
    src1 = "/home/parallels/stream_transfer/zero_globus/test_files1"
    src2 = "/home/parallels/stream_transfer/zero_globus/test_files2"
    src3 = "/home/parallels/stream_transfer/zero_globus/test_files3" """

    #src_path_all = '/home/parallels/stream_transfer/zero_globus/test_files'
    src_path = [src0, src1, src2, src3,src4, src5]
    #ep = [ep00, ep01, ep02, ep03]
    c1 = (src_path[0],ep[0])
    c2 = (src_path[1],ep[0])
    c3 = (src_path[2],ep[0])
    c4 = (src_path[3],ep[1])
    c5 = (src_path[4],ep[1])
    c6 = (src_path[5],ep[1])
    commands = [c1, c2, c3, c4, c5, c6]
    ep_count = 0
    src_count = 0
    #files = glob.glob(src_path)
    #if len(files) > 0 :
    #for ifile in files
    if one_endpoint:
       gl_refresh_chameleon.transfer(src_path_all,ep[0])
    else:
        while ep_count < 6:
            try:
                pid = os.fork()
                if pid == 0:
                    #gl_refresh_chameleon.transfer(src_path[ep_count],ep[ep_count])
                    #gl_refresh_chameleon.transfer(commands[ep_count])
                    print "this is priniting endpoint number: ", ep_count
                    os._exit(0)
                print "I am the parent process, and I just forked pid: ", pid

                    #gl_refresh.transfer(src_path[ep_count],ep[ep_count])
                    # gl_refresh.transfer(src_path[ep_count],ep[ep_count])
                ep_count += 1
            except OSError, e:

                print >>sys.stderr, "fork failed: %d (%s)" % (e.errno, e.strerror)
                sys.exit(1)
                #if ep_count == 4: break"""

if __name__ == "__main__":
    multi_transfer()
