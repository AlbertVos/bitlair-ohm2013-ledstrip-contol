#!/usr/bin/env python3

"""
export ADDR='[("192.168.94.106", 6454), ("192.168.94.104", 6454), ("192.168.94.100", 6454), ("192.168.94.105", 6454), ("192.168.94.103", 6454), ("192.168.94.102", 6454), ("192.168.94.101", 6454)]'

# Using the proxy:
export 'ADDR=[("192.168.94.2", 8000), ("192.168.94.2", 8001),("192.168.94.2", 8002),("192.168.94.2", 8003),("192.168.94.2", 8004),("192.168.94.2", 8005),("192.168.94.2", 8006)]'


cd data/python/ohm2013/strip/
export 'ADDR=[("192.168.1.108", 6454), ("192.168.1.109", 6454)]'
./proxy.py 

./fire.py 'addr=[("localhost", 8000)]'
./fire.py 'addr=[("localhost", 8001)]'

./fire.py 'addr=[("localhost", 8500)]'

"""

import socket
import time
import signal
import sys;
sys.path.append('../lib')
import select
import threading
import os
import random
import math
from strip import getAddr;


def hexdump(s):
    for b in xrange(0, len(s), 16):
        lin = [c for c in s[b : b + 16]]
        hxdat = ' '.join('%02X' % ord(c) for c in lin)
        pdat = ''.join((c if 32 <= ord(c) <= 126 else '.' )for c in lin)
        print( '  %04x: %-48s %s' % (b, hxdat, pdat) )
    print()


class Proxy:
  localHost = "0.0.0.0"
  localPort = 8000;
  broadcastPort = 8500;
  addr = [];
  socks = [];
  socksSrc = [];
  socksAddr = [];

  def __init__(self, addr_ = []):
    self.addr = getAddr(addr_);

    for i in range(len(self.addr)):
      # Convert hostname to ip address so when can compare it with address
      # data is received from.
      self.addr[i] = (socket.gethostbyname(self.addr[i][0]), self.addr[i][1]);

      sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM);
      sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1);
      #sock.setblocking(0);
      sock.bind((self.localHost, self.localPort + i));
      self.socks.append(sock);
      self.socksSrc.append(());
      self.socksAddr.append((self.localHost, self.localPort + i));
      print( "Channel ", self.socksAddr[i], " to ", self.addr[i] );

    # Add broadcast address to the lists
    
    # Local broadcast port
    broadcastAddr = (self.localHost, self.broadcastPort);
    # Address to broadcast to
    broadcastTo = ("", 6454);
    s = self.addr[0][0].split(".");
    s[3] = str(255);
    broadcastTo = (".".join(s), broadcastTo[1]);

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM);
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1);
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1);
    sock.bind(broadcastAddr);
    self.socks.append(sock);
    self.socksSrc.append(());
    self.addr.append(broadcastTo);
    self.socksAddr.append(broadcastAddr);
    i = len(self.socks) - 1;
    print( "Channel ", self.socksAddr[i], " to ", self.addr[i] );


  def run(self):
    while True:
      ready = select.select(self.socks, [], [], 0.5);
      index = -1;
      for i in range(len(ready[0])):
        s = ready[0][i];
        for j in range(len(self.socks)):
          if s == self.socks[j]:
            index = j;
            break
        if index >= 0:
          rdata, raddr = self.socks[index].recvfrom(5000);
          #print "received data from ", raddr, " @", self.socksAddr[index], \
          #  " to ", self.addr[index], " len=", len(rdata);
          #hexdump(rdata);

          # If address of received data is not the target address store it 
          # as the source address.
          #if (len(self.socksSrc[index]) == 0) and (raddr != self.addr[index]):
          #  self.socksSrc[index] = raddr;
          #  print "adding as src: ", raddr;
          if raddr != self.addr[index]:
            self.socksSrc[index] = raddr;
          if (raddr == self.socksSrc[index]) and (len(self.socksSrc[index]) > 0):
            #print "Send to ", self.addr[index];
            self.socks[index].sendto(rdata, self.addr[index]);
          elif (raddr == self.addr[index]) and (len(self.addr[index]) > 0):
            #print "Send to ", self.socksSrc[index];
            self.socks[index].sendto(rdata, self.socksSrc[index]);
          else:
            print( "Unknown address", raddr )


def signal_handler(signal_, frame):
  os.kill(os.getpid(), signal.SIGKILL);
  sys.exit(0)

if __name__ == "__main__":
  signal.signal(signal.SIGINT, signal_handler)
  p = Proxy();
  p.run();


