import os
import sys
import multiprocessing as mp
import time

##============================================================================##
##----------------------------- globus_urlcopy -------------------------------##
##============================================================================##

'''
Purpose:             Calling globus urlcopy with specific endpoints

Author:               Yuliana Zamora
Email:                yzamora@uchicago.edu
Date Created:         August 24, 2017
Date Last Modified:   September 17, 2017
'''
#globus-url-copy -vb -p 10 ftp://129.114.33.196:50003/dev/zero ftp://140.221.68.225:50003/dev/null
##============================================================================##
##------------------------------globus_urlcopy---- ---------------------------##
##============================================================================##

n_processes = 4 #Number of globus transfer done in parallel - performance limit is VCPUs available
tran_size= 10 #limit amount that will be transfered. Thiis is in GB

def myfunc(i, p, src, port, dest):
    os.system('globus\-url\-copy \-vb \-len ' + str(tran_size) + 'GB \-p' + ' ' + str(p) + ' ' + '\-cc 1' + ' ' + 'ftp://' + src + ':' + port + '/dev/zero' + ' ' + 'ftp://' + dest + ':' + port + '/dev/null'  )

    print "Process: ", i, "is done"

#def ucopy(source,destination,port):
def ucopy(source, destination, port, par):
    ips = {}
    cooley = {}
    with open("cham_ports", 'r') as f:
        for line in f:
            key = line.split()[0]
            value = line.split()[1]
            ips[key] = value
    with open("cooley_ports",'r') as c:
        for line in c:
            key = line.split()[0]
            value = line.split()[1]
            cooley[key] = value
    #n_processes = 4
    myprocs = []
    for i in range(0, n_processes):
        p = mp.Process(target=myfunc,args=(i,par,ips[source],port,cooley[destination]))
        myprocs.append(p)
        p.start()
        print " -c -> ",i%mp.cpu_count()," -p ->",p.pid
        os.system("taskset -p -c "+str(i%mp.cpu_count())+" "+str(p.pid)) 
        #p.start()
    #os.system('globus\-url\-copy \-vb \-p' + ' ' +  p + ' ' + '\-cc 1' + ' ' + 'ftp://' + ips[source] + ':' + port + '/dev/zero' + ' ' + 'ftp://' + cooley[destination] + ':' + port + '/dev/null'  )
    for p in myprocs: p.join()
    
def userver(port):              
    os.system('globus\-gridftp\-server -\debug \-aa \-p' + ' ' + port) 

if __name__ == '__main__':
    #ucopy("yulie1","yulie2",50001)
    if len(sys.argv)>2:
        source = sys.argv[1]
        destination = sys.argv[2]
        port = sys.argv[3]
        p = sys.argv[4]
        start = time.time()
        ucopy(source, destination, port,p)
        etime = time.time()
        tt = etime - start
        print "Total time : ", tt
        print "Transfer Rate Calculated: ", (1000.00*tran_size)/tt, "MB/sec"  
    else:
        port = sys.argv[1]
        userver(port)
