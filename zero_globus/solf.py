import os
import sys
import time
import split_stream

filename = 'bigfile_test'
src_path = '/home/parallels/stream_transfer/zero_globus/test_files'
nfiles = 3

def stream_file():

    for ifile in xrange(nfiles):
        fname_src = src_path + '/' + filename + '.' + str(ifile)

        print('Creating file')
        with open(fname_src, 'wr+') as f:
            while int(os.stat(fname_src).st_size) < 1000000000:
                iline = 0
                f.write('Adding line ' + str(iline) + ' in ' + filename
                                       + '.' + str(ifile) + '\n')
                f.flush()
                iline += 1
            #if int(os.path.getsize(fname_src)) > 1000: break
                a = os.path.getsize(fname_src)
                #print "Size of file is: ", a
    print 'All files Done.(solf.py)'


if __name__ == "__main__":
    stream_file()
