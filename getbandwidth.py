import sys
import os
import datetime
import time
import json
import commands
from ifparser import Ifcfg

lines = []

"""with open('bw.out', 'r') as f:
    lines = f.readlines()
"""
with open('rx_values', 'ab') as r:
    with open('tx_values', 'ab') as t:
    #f.writelines(lines[:1] + lines[2:])
    #f.writelines("the time is" + str(st) + "\n")
    starting_rx =
    starting_tx =
        while True:
            time.sleep(1)
            ts = time.time()
            st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            ifdata = Ifcfg(commands.getoutput('ifconfig -a'))
            interfacelist = ifdata.interfaces
            #print "this is other interface is list \n", interfacelist
            #print "these are rx bytes", ifdata.get(itype='RX bytes:')
            eth = ifdata.get_interface('enp0s5')
            eth0 = eth.get_values()
            r.writelines('Time: ' + str(st) + ' Values: ' + 'RX bytes: '+ str(eth0[u'rxbytes']) + "\n")
            t.writelines('Time: ' + str(st) + ' Values: '+ 'TX bytes: '+ str(eth0[u'txbytes']) + "\n")
            #data = json.loads(eth0)
            #print "this is eth0 values:", eth0
            print "this is rx value:", eth0[u'rxbytes']
            print "this is tx value:", eth0[u'txbytes']
