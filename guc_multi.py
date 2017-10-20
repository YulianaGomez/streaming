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
Date Last Modified:   September 22, 2017
'''
#globus-url-copy -vb -p 10 ftp://129.114.33.196:50003/dev/zero ftp://140.221.68.225:50003/dev/null
##============================================================================##
##------------------------------globus_urlcopy---- ---------------------------##
##============================================================================##


## INPUT OPTIONS TO LOOP THROUGH:
min_delay = 120 #120   #wait 2 mins between transfers
procs_in  = [1]   #Number of globus transfer done in parallel - performance limit is VCPUs available
size_in   = [10]   #limit amount that will be transfered. This is in GB
par_in    = [1,2,4,6,8,10] #[1,2,4,6,8,10]   #parallelism settings


def myfunc(i, p, src, port, dest, tran_size):
    local_ti = time.time()
    os.system('globus\-url\-copy \-vb \-len ' + str(tran_size) + 'GB \-p' + ' ' + str(p) + ' ' + '\-cc 1' + ' ' + 'ftp://' + src + ':' + port + '/dev/zero' + ' ' + 'ftp://' + dest + ':' + port + '/dev/null'  )
    local_tf = time.time()
    local_tt = local_tf - local_ti
    print "Process: ", i, "is done in ",local_tt," sec"

#def ucopy(source,destination,port):
def ucopy(source, destination, port, np, tran_size, par):
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
    myprocs = []
    for i in range(0, np):
        p = mp.Process(target=myfunc,args=(i,par,ips[source],port,cooley[destination],tran_size))
        myprocs.append(p)
        p.start()
        os.system("taskset -p -c "+str(i%mp.cpu_count())+" "+str(p.pid)) 
    for p in myprocs: p.join()
    
def userver(port):              
    os.system('globus\-gridftp\-server -\debug \-aa \-p' + ' ' + port) 

if __name__ == '__main__':

    # Remove send.done and send.exit (if they exist):
    if os.path.exists('./send.done'):
        os.system('rm send.done')
    if os.path.exists('./send.exit'):
        os.system('rm send.exit')

    time_last = time.time()
    send_cnt = 0

    #ucopy("yulie1","yulie2",50001)
    if len(sys.argv)>2:
        source = sys.argv[1]
        destination = sys.argv[2]
        port = sys.argv[3]
        # Look for commandline p input if par_in is empty:
        if par_in == []:
            p = sys.argv[4]
            par_in.append(p)
        # Loop through all options of interest
        for np in procs_in:
            for tran_size in size_in:
                for p in par_in:
                    while True:
                        if send_cnt == 0: break
                        thistime = time.time() 
                        if thistime - time_last > min_delay: 
                            time_last = thistime 
                            break
                    print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
                    print "np ", np," size ", tran_size," p ", p
                    print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
                    sys.stdout.flush() # FLUSH  
                    os.system('iostat')
                    sys.stdout.flush() # FLUSH
                    start = time.time()
                    ucopy(source, destination, port, np, tran_size, p)
                    etime = time.time()
                    tt = etime - start
                    sys.stdout.flush() # FLUSH
                    os.system('uptime')
                    sys.stdout.flush() # FLUSH
                    os.system('iostat')
                    sys.stdout.flush() # FLUSH
                    print "Total time : ", tt
                    # 1GB = 1073741824 B ->
                    totalbw = (1073.74 * float(tran_size) * float(np)) / float(tt)
                    print "Transfer Rate Calculated: ", totalbw, "MB/sec" 
                    sys.stdout.flush() # FLUSH
                    os.system('touch send.done')
                    send_cnt += 1
        os.system('touch send.exit')
        print 'Finishing Normally.'
    else:
        port = sys.argv[1]
        userver(port)
        sys.exit(0)

