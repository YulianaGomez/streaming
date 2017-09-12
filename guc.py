import os
import sys


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

#def ucopy(source,destination,port):
def ucopy(source, destination, port):
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

    os.system('globus\-url\-copy \-vb \-p 10' + ' ' + 'ftp://' + ips[source] + ':' + port + '/dev/zero' + ' ' + 'ftp://' + cooley[destination] + ':' + port + '/dev/null'  )

if __name__ == '__main__':
    #ucopy("yulie1","yulie2",50001)
    source = sys.argv[1]
    destination = sys.argv[2]
    port = sys.argv[3]
    ucopy(source, destination, port)
