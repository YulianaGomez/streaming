import os
import sys
from multiprocessing import Process


##============================================================================##
##----------------------------- globus_urlcopy -------------------------------##
##============================================================================##

'''
Purpose:             Calling globus urlcopy with specific endpoints

Author:               Yuliana Zamora
Email:                yzamora@uchicago.edu
Date Created:         August 24, 2017
Date Last Modified:   August 24, 2017
'''
#globus-url-copy -vb -p 10 ftp://129.114.33.196:50003/dev/zero ftp://140.221.68.225:50003/dev/null
##============================================================================##
##------------------------------globus_urlcopy---- ---------------------------##
##============================================================================##
i
def f(p, src, port, dest):
    os.system('globus\-url\-copy \-vb \-p' + ' ' +  p + ' ' + '\-cc 1' + ' ' + 'ftp://' + src + ':' + port + '/dev/zero' + ' ' + 'ftp://' + dest + ':' + port + '/dev/null'  )


#def ucopy(source,destination,port):
def ucopy(source, destination, port,p):
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

    n_processes = 4
    myprocs = []
    for i in range(0, n_processes):
        p = Process(target=f,args=(p,ips[source],port,cooley[destination]))
        myprocs.append(p)
        os.system("taskset -c %d -p %d" % ((i % os.cpu_count()), p.pid)) 
        p.start()
    #os.system('globus\-url\-copy \-vb \-p' + ' ' +  p + ' ' + '\-cc 1' + ' ' + 'ftp://' + ips[source] + ':' + port + '/dev/zero' + ' ' + 'ftp://' + cooley[destination] + ':' + port + '/dev/null'  )
    #for p in myprocs: p.join()
    
def userver(port):              
    os.system('globus\-gridftp\-server -\debug \-aa \-p' + ' ' + port) 

if __name__ == '__main__':
    #ucopy("yulie1","yulie2",50001)
    if len(sys.argv)>2:
        source = sys.argv[1]
        destination = sys.argv[2]
        port = sys.argv[3]
        p = sys.argv[4]
        ucopy(source, destination, port,p)
    else:
        port = sys.argv[1]
        userver(port)
