import os
import sys
import time
import split_stream

##============================================================================##
##----------------------------- streamonefile.py -----------------------------##
##============================================================================##

'''
Purpose:              "Stream" <nfiles> of <nlines> length into <src_path>

Author:               Yuliana Zamora
Email:                yzamora@uchicago.edu
Date Created:         June 25, 2017
Date Last Modified:   June 28, 2017
'''

run_split = True   # Set to True to run 'split_stream.py' by running this
filename  = 'filename_test'
src_path  = '/home/parallels/stream_transfer/zero_globus/test_files2'
#src_path  = './test_files_src'
nfiles    = 1
nlines    = 1000   # Set to zero to stream until 'end_time'
end_time  = 120
delay     = 0.01   # delay between writing each line

##============================================================================##
##--------------------------------- one_file() -------------------------------##
##============================================================================##

def one_file():

    timeout  = time.time() + end_time

    for ifile in xrange(nfiles):

        fname_src = src_path + '/' + filename + '.' + str(ifile)

        print('Creating File')
        with open(fname_src,'wr+') as f:

            iline = 0
            while time.time() < timeout:

                f.write('Adding line ' + str(iline) + ' in ' + filename
                                       + '.' + str(ifile) + '\n')
                print('Adding line: ', iline)
                iline += 1
                time.sleep(delay)
                if (nlines <> 0) and (iline == nlines): break

    print 'All files Done.(streamonefile)'

################################################################################
##============================================================================##
##------------------------------------ MAIN ----------------------------------##
##============================================================================##
################################################################################

if __name__ == "__main__":

    if not run_split:
        one_file(); sys.exit(0)

    try:

        pid = os.fork()

        if pid == 0:

            one_file()
            os._exit(0)

        else:

            split_stream.manage_split()

    except OSError, e:

        print >>sys.stderr, "fork failed: %d (%s)" % (e.errno, e.strerror)
        sys.exit(1)
