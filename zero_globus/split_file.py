import os
import sys
import glob

##============================================================================##
##------------------------------- stream_data.py -----------------------------##
##============================================================================##
'''
Purpose:              Splitting up a file by byte sizes and creating new file of
                      specific byte size.

Author:               Yuliana Zamora
Email:
Date Created:         June 25, 2017
Date Last Modified:   June 25, 2017
'''

################################################################################
##============================================================================##
##------------------------------------ MAIN ----------------------------------##
##============================================================================##
################################################################################

def split_file(files):
    #dest_path = "/home/parallels/stream_transfer/zero_globus/destination/"
    dest_path = "/Users/yzamora/streaming/zero_globus/destination/"
    chunksize = 100
    offset = 0 
    iter = 0
    for curFile in files:
    	cfile = open(curFile, "r")
    	data = cfile.read(chunksize)
    	while data != '':
    	    #Taking specific chunk of data
    	    cfile.seek(offset,os.SEEK_SET)
    	    data = cfile.read(chunksize)
            #Putting specific chunk size of data into file
            iter += 1
            fn = dest_path+"filename."+str(iter)
            f = open(fn,'wb')
            f.write(data)
            print("Creating file=" + fn)
            offset+=len(data)
            

        if data=='':
            print("End of final file transfer; File=" + fn)

        f.close()
        print("%i bytes transferred"%offset)
    		#Read chunk of data from file





#################MAIN METHOD#########################

if __name__=='__main__':
	files = glob.glob('/Users/yzamora/streaming/zero_globus/test_files/*')
	if len(files)>0:
	    split_file(files)
###################################

