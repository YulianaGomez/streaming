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
    dest_path = "/home/parallels/stream_transfer/zero_globus/test_files/"
    chunksize = 100
    offset = 0
    iter = 0
    #print("Splitting data into bytes will begin")
    for curFile in files:
    	cfile = open(curFile, "rb")
    	data = cfile.read(chunksize)
        #print("Currently in split_stream in for loop")
    	while data!='':
            #if data!='':
            print("Getting specific byte size of file and putting into file")
	        #Taking specific chunk of data
            cfile.seek(offset,os.SEEK_SET)
            data = cfile.read(chunksize)
            #Putting specific chunk size of data into file
            iter += 1
            fn = dest_path+"filename."+str(iter)
            f = open(fn,'wb')
            print("Putting data into file")
            f.write(data)
            print("Creating file=" + fn)
            print("Incrementing offset")
            print("%i bytes transferred into filename: %s"%(offset,fn))
            offset+=len(data)
            if data=='':
                print("End of final file transfer")
                #break
            f.close()
            #os._exit(0)

    		#Read chunk of data from file





#################MAIN METHOD#########################

if __name__=='__main__':
    while True:
        files = glob.glob('/home/parallels/stream_transfer/zero_globus/test_files2/*')
        if len(files)>0:
            split_file(files)
###################################
