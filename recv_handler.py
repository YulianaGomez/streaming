"""
recv_handler.py
This is just  script to wait for the send_handler.py
script to create the send.done file. When the file exists,
we remove it, and then read the CPU load and IO status.

Author: Yuliana Zamora
Email: yzamora@uchicago.edu
Last worked on: Sept 22th, 2017
"""
import os
import time

officialrun = True
#officialrun = False

##
## MAIN:
##

if officialrun:

    if os.path.exists('./transition.summary'):
        os.system('mv transition.summary old.transition.summary')

    cpid = os.fork()
    if cpid == 0:
        os.system('python guc_multi.py 4vcpu cc028 50001 >transfer.summary 2>&1')
        os._exit(0)

    # Remove old 'summary.out' if it exists:
    if os.path.exists('./summary.out'):
        os.system('mv summary.out old.summary.out')
    if os.path.exists('./send.done'):
        os.system('rm send.done')
    if os.path.exists('./send.exit'):
        os.system('rm send.exit')

    while True:

        # If 'send.done' exists, remove it and call getinfo.sh:
        if os.path.exists('./send.done'):
            os.system('rm send.done')
            os.system('./getinfo.sh >> summary.out')
            print 'getinfo.sh output appended to summary.out..'
 
        # If 'send.exit' exists, break:
        if os.path.exists('./send.exit'): break

        #print 'recv_handler is.. sleeping'
        time.sleep(4)

    print 'recv_handler is exiting normally.'
    os.waitpid(cpid, os.WNOHANG)

# Process transfer.summary:
print '\n'
print '\n'
print 'Processing transfer.summary'
results = {}
with open('transfer.summary','r') as f:
    data = f.readlines()
    localbw = 0.0
    nlocal = 0
    np = 0
    tran_size = 0
    par = 0
    i_io = 0; kbr_i=0; kbw_i=0
    for line in data:
        items = line.split()
        if len(items) > 0 and items[0] == 'np':
            np = int(items[1])
            tran_size = int(items[3])
            par = int(items[5])
            results[(np,tran_size,par)] = [] 
        elif len(items) > 4 and items[3] == 'MB/sec':
            localbw += float(items[2])
            nlocal += 1
        elif 'average:' in items:
            for it in range(len(items)):
                if items[it] == 'average:':
                    cpuload = items[it+1].split(',')[0]
                    results[(np,tran_size,par)].append(cpuload)
                    break
            print 'cpuload =',cpuload
        elif len(items) > 5 and items[0] == 'vda':
            kbread = int(items[4])
            kbwrtn = int(items[5])
            if i_io == 0:
                kbr_i = kbread
                kbw_i = kbwrtn
            else:
                kbread -= kbr_i
                kbwrtn -= kbw_i
                results[(np,tran_size,par)].append(kbread+kbwrtn)
            i_io+=1
            print 'ioval =',kbread+kbwrtn
        elif len(items) > 3 and items[2] == 'Calculated:':
            globalbw = float(items[3])
            localbw = localbw / float(np)
            results[(np,tran_size,par)].append(localbw)
            results[(np,tran_size,par)].append(globalbw)
            localbw = 0.0
            nlocal = 0
            np = 0
            tran_size = 0
            par = 0
            i_io = 0; kbr_i=0; kbw_i=0

print 'np,tran_size,par,cpuload,ioval,localbw,globalbw'
for key, value in results.iteritems():
    (np,tran_size,par) = key
    (cpuload,ioval,localbw,globalbw) = value
    print np,tran_size,par,cpuload,ioval,localbw,globalbw


