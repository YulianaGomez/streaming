import os
#from globus_sdk import (TransferClient, TransferAPIError, TransferData, DeleteData, AccessTokenAuthorizer)
import os.path
#import globus_sdk
import glob
from pathlib import Path
from os import makedirs
import gl_refresh

ep00 = "dffc2d9c-689e-11e7-a9ab-22000bf2d287"
ep01 = "2dad0d9a-689f-11e7-a9ab-22000bf2d287"
ep02 = "6f8b5afa-689f-11e7-a9ab-22000bf2d287"
ep03 = "89c4b542-689f-11e7-a9ab-22000bf2d287"
src_path = '/home/parallels/stream_transfer/zero_globus/test_files'
ep = [ep00, ep01, ep02, ep03]
def multi_transfer():
    ep_count = 0
    #files = glob.glob(src_path)
    #if len(files) > 0 :
    #for ifile in files:
    while ep_count < 4:
        gl_refresh.transfer("/home/parallels/stream_transfer/zero_globus/test_files",ep[ep_count])
        ep_count += 1
    #if ep_count == 4: break

if __name__ == "__main__":
    multi_transfer()
