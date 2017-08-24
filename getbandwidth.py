import sys
import os
import datetime
import time
import json
import commands
from ifparser import Ifcfg

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
            pd = False #set to true if you want all details written into file
            total = False # set to true if you want total bw usage in file
            bw = True # set true when want bw utilization
            totalbw_rx = 0
            totalbw_tx = 0
            ts = time.time()
            st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            ifdata = Ifcfg(commands.getoutput('ifconfig -a'))
            interfacelist = ifdata.interfaces
            eth = ifdata.get_interface('ens3')
            eth0 = eth.get_values()
            starting_rx= eth0[u'rxbytes']
            starting_tx = eth0[u'txbytes']
            timeout = time.time() + end_time
            while time.time() < timeout:
                time.sleep(1)
                ts = time.time()
                st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
                ifdata = Ifcfg(commands.getoutput('ifconfig -a'))
                interfacelist = ifdata.interfaces
                #print "this is other interface is list \n", interfacelist
                #print "these are rx bytes", ifdata.get(itype='RX bytes:')
                eth = ifdata.get_interface('ens3')
                eth0 = eth.get_values()
                cur_rx = eth0[u'rxbytes']
                cur_tx = eth0[u'txbytes']
                if totalbw_rx == 0 and totalbw_tx == 0:
                    if bw:
                        bw_rx = int(cur_rx) - int(starting_rx)
                        newrx = cur_rx

                        bw_tx = int(cur_tx) - int(starting_tx)
                        newtx = cur_tx
                        r.writelines(str(bw_rx) + '\n')
                        t.writelines(str(bw_tx) + '\n')
                    else:
                        totalbw_rx +=  int(cur_rx) - int(starting_rx)
                        newrx = cur_rx

                        totalbw_tx +=  int(cur_tx) - int(starting_tx)
                        newtx = cur_tx
                else:
                    totalbw_rx += int(cur_rx) - int(newrx)
                    totalbw_tx += int(cur_tx) - int(newtx)
                if pd:
                    r.writelines('Time: ' + str(st) + ' Values: ' + 'RX bytes: '+ str(eth0[u'rxbytes']) + " Total RX: " + str(totalbw_rx) + "\n")
                    t.writelines('Time: ' + str(st) + ' Values: '+ 'TX bytes: '+ str(eth0[u'txbytes']) + " Total TX: " + str(totalbw_tx) +"\n")
                elif total:
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
