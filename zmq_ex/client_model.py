"""CLIENT waiting for msg, sending requests ahead as credits,

Author: Yuliana Zamora
Email: yzamora@uchicago.edu
Last worked on: June 12, 2017
"""

import os
import sys
from threading import Thread

import zmq

from zhelpers import socket_set_hwm, zpipe

DEFAULT_CHUNK_SIZE=1024
DEFAULT_OUTPUT_DIR="/home/parallels/yzamora/streaming/destination/"
DEFAULT_DEST_ADDR="34.207.160.51"
DEFAULT_DEST_PORT="10120"

def client(chunk_size, output_dir, dest_addr, dest_port):
    destroot = output_dir #my machine 

    ctx = zmq.Context()
    dealer = ctx.socket(zmq.DEALER)
    socket_set_hwm(dealer, 0)
    addr_full = "tcp://" + dest_addr + ":" + dest_port
    dealer.connect(addr_full)
    total = 0       # Total bytes received
    chunks = 0      # Total chunks received

    # file loop
    while True:
       dealer.send_multipart([
           b"fetch",
           b"%i" % chunk_size
       ])

       msg = dealer.recv_multipart()
       [fname, status] = msg
       if status != "ready":
           print("something wrong!")
           sys.exit(1)

       filestrs = fname.split('/')
       fn = destroot+filestrs[len(filestrs)-1]
       f = open(fn, 'wb')
       print("Creating file=" + fn)

       # chunk loop 
       while True:
           dealer.send_multipart([
              b"transfer", 
              b"%i" %total
           ])
           try:
               try:
                   msg = dealer.recv_multipart()
               except zmq.ZMQError as e:
                   if e.errno == zmq.ETERM:
                       return
                   else:
                       raise
               [data] = msg
               #print("Received msg size=" + str(len(data)))
   
               if data=='':
                  print("End of file transfer; File=" + fn)
                  break

               f.write(data)
               total += len(data)
           except zmq.ZMQError as e:
               if e.errno == zmq.ETERM:
                   return   # shutting down, quit
               else:
                   raise
       f.close()
       print("%i bytes received" % total)
       total=0


###################MAIN METHOD##########################
def main():
   if len(sys.argv)<5:
      print("Usage: python " + sys.argv[0] + " <chunk-size="+str(DEFAULT_CHUNK_SIZE) + "> <output-dir="+ DEFAULT_OUTPUT_DIR + "> <dest-address=" + DEFAULT_DEST_ADDR + "> <dest-port=" + DEFAULT_DEST_PORT + ">")
      sys.exit(0)

   chunk_size = int(sys.argv[1])
   if chunk_size==0: chunk_size=DEFAULT_CHUNK_SIZE

   output_dir = sys.argv[2]
   if len(output_dir)==0: output_dir=DEFAULT_OUTPUT_DIR

   dest_addr = sys.argv[3]
   if len(dest_addr)==0: dest_addr=DEFAULT_DEST_ADDR

   dest_port = sys.argv[4]
   if len(dest_port)==0: dest_port=DEFAULT_DEST_PORT

   client(chunk_size, output_dir, dest_addr, dest_port)



if __name__ == '__main__':
    main()
