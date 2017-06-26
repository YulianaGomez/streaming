import os
import sys
import glob
import subprocess

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

"""
GLOBUS COMMAND
globus-url-copy -off 0 -len 1 -s "/C=US/O=Globus Consortium/OU=Globus
Connect Service/CN=6f52ca68-5a90-11e7-bf20-22000b9a448b"
gsiftp://localhost:2811/home/parallels/stream_transfer/test_files/test1.txt ./test2
"""
"""
FIRST DO EXPORT:
export X509_CERT_DIR=/var/lib/globus-connect-server/grid-security/certificates
"""

def split_file(files):
    os.environ["X509_CERT_DIR"]="var/lib/globus-connect-server/grid-security/certificates"
    src_path = "/home/parallels/stream_transfer/zero_globus/test_files/"
    dest_path = "/home/parallels/stream_transfer/zero_globus/destination/"
    chunksize = 10000
    offset = 0
    iter = 0
    for curFile in files:
        print "in for loop", curFile
    	#cfile = open(curFile, "r")
        #data = cfile.read(chunksize)
    	while True:
            #if data!='':
            	cmd = []
                cmd.append('globus-url-copy')
                cmd.append('-off')
                cmd.append(str(offset))
                cmd.append('-len')
                cmd.append(str(chunksize))
                cmd.append('-s')
                cmd.append('/C=US/O=Globus Consortium/OU=Globus Connect Service/CN=6f52ca68-5a90-11e7-bf20-22000b9a448b')
                cmd.append('gsiftp://localhost:2811/'+src_path)
                cmd.append(dest_path)
                subprocess.call(cmd)
    	        #Taking specific chunk of data
    	        #cfile.seek(offset,os.SEEK_SET)
    	        #data = cfile.read(chunksize)
                #Putting specific chunk size of data into file
                iter += 1
                #fn = dest_path+"filename."+str(iter)
                #f = open(fn,'wb')
                #f.write(data)
                #print("Creating file=" + fn)
                offset+=1000


        #if data=='':
            #print("End of final file transfer; File=" + fn)

        f.close()
        print("%i bytes transferred"%offset)
    		#Read chunk of data from file





#################MAIN METHOD#########################

if __name__=='__main__':
    while True:
        files = glob.glob('/home/parallels/stream_transfer/zero_globus/test_files/*')
        if len(files)>0:
            split_file(files)
###################################
