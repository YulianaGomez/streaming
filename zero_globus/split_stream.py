import os
import sys
import time
import glob
import subprocess

##============================================================================##
##------------------------------ split_stream.py -----------------------------##
##============================================================================##

'''
Purpose:              Copies files existing in 'src_path' into a series of
                      smaller files in 'dest_path'

Author:               Yuliana Zamora
Email:                yzamora@uchicago.edu
Date Created:         June 25, 2017
Date Last Modified:   June 30, 2017
'''

src_path  = '/home/parallels/stream_transfer/zero_globus/test_files2'
dest_path = '/home/parallels/stream_transfer/zero_globus/test_files'
#src_path  = './test_files_src'
#dest_path = './test_files_dest'
chunksize = 1000
time_out  = 5      # End if <src_path> is empty for <time_out> [s]
time_frm  = 5      # RM file if it is unchanged for <time_frm> [s]

##============================================================================##
##-------------------------------- split_file() ------------------------------##
##============================================================================##

def split_file(files, file_history):

    # Loop over files in <src_path>
    for curFile in files:

        # Separate the filename from the full path
        filename = os.path.basename(curFile)

        # Update/Get info from file_history
        if curFile in file_history:

            iter = file_history[curFile]['iter']
            offset = file_history[curFile]['offset']

        else:

            file_history[curFile] = {}
            iter = 0
            offset = 0
            file_history[curFile]['reftime'] = time.time()

        # Copy info in loop (start from current offest)
        while True:

            cfile = open(curFile, 'rb')
            cfile.seek(offset,os.SEEK_SET)
            data = cfile.read(chunksize)

            if data!='':

                iter += 1
                fn = dest_path + '/' + filename + '.' + str(iter)
                f = open(fn,'wb')
                f.write(data)
                f.close()
                print('%i bytes transfered into %i file'%(offset,iter))
                offset += len(data)
                file_history[curFile]['reftime'] = time.time()

            else:

                file_history[curFile]['iter'] = iter
                file_history[curFile]['offset'] = offset
                reftime = file_history[curFile]['reftime']
                if((time.time() - reftime) > time_frm):
                    subprocess.call(['rm',curFile])
                break

##============================================================================##
##------------------------------ manage_split() ------------------------------##
##============================================================================##

def manage_split():

    # Define empty dict to store history of 'split' files
    file_history = {}

    # Reference time
    ref_time = time.time()

    # Wait for files to split
    while True:

        # Get list of any files existing in <src_path>
        files = glob.glob(src_path+'/*')

        # Try to split files if they are present
        if len(files) > 0:

            split_file(files, file_history)
            ref_time = time.time()

        else:

            empty_time = time.time()
            if((empty_time - ref_time) > time_out):
                print 'Done transfering data. (split_stream)'
                break


################################################################################
##============================================================================##
##------------------------------------ MAIN ----------------------------------##
##============================================================================##
################################################################################

if __name__=='__main__': manage_split()
