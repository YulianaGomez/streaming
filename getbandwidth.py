import sys
import os
import datetime
import time
import json
import commands
from ifparser import Ifcfg
import plot_bw

##============================================================================##
##----------------------------- getbandwidth.py -----------------------------##
##============================================================================##

'''
Purpose:             Getting bandwidth utilization of system

Author:               Yuliana Zamora
Email:                yzamora@uchicago.edu
Date Created:         August 23, 2017
Date Last Modified:   August 24, 2017
'''

end_time = 30 #number of seconds to run program

##============================================================================##
##--------------------------------- getbw----- -------------------------------##
##============================================================================##


def getbw():
    with open('rx_values', 'ab') as r:
        with open('tx_values', 'ab') as t:
            with open('time.out', 'ab') as ti:
                pd = False #set to true if you want all details written into file
                total = False # set to true if you want total bw usage in file
                bw = True # set true when want bw utilization
                totalbw_rx = 0
                totalbw_tx = 0
                ts = time.time()
                st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
                ifdata = Ifcfg(commands.getoutput('ifconfig -a'))
                interfacelist = ifdata.interfaces
                eth = ifdata.get_interface('eno1')
                eth0 = eth.get_values()
                starting_rx= eth0[u'rxbytes']
                starting_tx = eth0[u'txbytes']
                timeout = time.time() + end_time
                while time.time() < timeout:
                    #time.sleep(1)
                    #ts = time.time()
                    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
                    ifdata = Ifcfg(commands.getoutput('ifconfig -a'))
                    interfacelist = ifdata.interfaces
                    #print "this is other interface is list \n", interfacelist
                    #print "these are rx bytes", ifdata.get(itype='RX bytes:')
                    #eth = ifdata.get_interface('ens3')
                    eth = ifdata.get_interface('enp0s5')
                    eth0 = eth.get_values()
                    cur_rx = eth0[u'rxbytes']
                    cur_tx = eth0[u'txbytes']

                    #obtaining bw utilization per second
                    if bw:
                         if totalbw_rx == 0 and totalbw_tx == 0:
                             t2 = time.time()
                             ct = t2-ts
                             bw_rx = int(cur_rx) - int(starting_rx)
                             newrx = cur_rx
                             bw_tx = int(cur_tx) - int(starting_tx)
                             newtx = cur_tx
                             r.writelines(str(bw_rx) + '\n')
                             t.writelines(str(ct) + '\t' + str(bw_tx)  + '\n')
                             #ti.writelines(str(ct) + '\n')
                             totalbw_rx = 1
                             totalbw_tx = 1

                         else:
                             t2 = time.time()
                             ct = t2-ts
                             bw_rx = int(cur_rx) - int(newrx)
                             bw_tx = int(cur_tx) - int(newtx)
                             newrx = cur_rx
                             newtx = cur_tx
                             r.writelines(str(bw_rx) + '\n')
                             t.writelines(str(ct) + '\t' + str(bw_tx)  + '\n')
                             #ti.writelines(str(ct) + '\n')

                    #Getting initial total bw results
                    elif total:
                        print "In total loop"
                        if totalbw_rx == 0 and totalbw_tx == 0:
                            totalbw_rx +=  int(cur_rx) - int(starting_rx)
                            newrx = cur_rx

                            totalbw_tx +=  int(cur_tx) - int(starting_tx)
                            newtx = cur_tx
                        #accumulating total bw
                        else:
                            print "In total else loop"
                            totalbw_rx += int(cur_rx) - int(newrx)
                            totalbw_tx += int(cur_tx) - int(newtx)

                    #decing whether to write detail output (pd) or just total bw (total)
                    if pd:
                        print "In pd print loop"
                        r.writelines('Time: ' + str(st) + ' Values: ' + 'RX bytes: '+ str(eth0[u'rxbytes']) + " Total RX: " + str(totalbw_rx) + "\n")
                        t.writelines('Time: ' + str(st) + ' Values: '+ 'TX bytes: '+ str(eth0[u'txbytes']) + " Total TX: " + str(totalbw_tx) +"\n")
                    elif total:
                        print "In total print loop"
                        r.writelines(str(totalbw_rx) + '\n')
                        t.writelines(str(totalbw_tx) + '\n')

                    #data = json.loads(eth0)
                    #print "this is eth0 values:", eth0
                    print "this is rx value:", eth0[u'rxbytes']
                    print "this is tx value:", eth0[u'txbytes']

##============================================================================##
##--------------------------------- MAIN--------------------------------------##
##============================================================================##
if __name__ == "__main__":
        getbw()
        print "I'm all done"
        plot_bw.plot_bw()
