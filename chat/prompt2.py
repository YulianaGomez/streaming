import zmq
import random

def main(addr1, addr2, who):
#Creating two sockets
#Socket 1
   ctx = zmq.Context()
   socket = ctx.socket(zmq.PUB)
   socket.bind("tcp://127.0.0.1:%s" % addr1)
#Socket 2
   ctx2 = zmq.Context()
   socket2 = ctx2.socket(zmq.PUB)
   socket2.bind("tcp://127.0.0.1:%s" % addr2)


   while True:
        msg = raw_input("%s> " % who)
        if random.randint(1,2) == 1:
            socket.send_pyobj((msg, who))
        else:
            socket2.send_pyobj((msg, who))


if __name__ == '__main__':
#    import sys
#    if len(sys.argv) != 3:
#        print "usage: prompt.py <address> <username>"
#        raise SystemExit
    #main(sys.argv[1], sys.argv[2])
    main(10111, 10112, "kyle")
