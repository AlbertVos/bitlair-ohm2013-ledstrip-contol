#!/usr/bin/python

"""
export ADDR='[("192.168.94.106", 6454), ("192.168.94.104", 6454), ("192.168.94.100", 6454), ("192.168.94.105", 6454), ("192.168.94.103", 6454), ("192.168.94.102", 6454), ("192.168.94.101", 6454)]'
"""

import socket
import time
import signal
import sys
import select
import threading
import os
import random
import math


class Proxy:
  localHost = "0.0.0.0"
  localPort = 8000;
  addr = [];
  socks = [];
  socksSrc = [];
  socksAddr = [];

  def __init__(self, addr_ = []):
    if len(addr_) > 0:
      self.addr = addr_;
    if "ADDR" in os.environ:
      self.addr = self.toTuppleArray(os.environ.get('ADDR'));
    if len(sys.argv) > 1:
      for i in range(1, len(sys.argv)):
        if sys.argv[i].startswith("addr="):
          self.addr = self.toTuppleArray(sys.argv[i][5:]);
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
      print "Channel ", self.socksAddr[i], " to ", self.addr[i];

  def toTuppleArray(self, s):
    if ((s[0] == '"') or (s[0] == "'")):
      s = "[(" + s + ")]";
    elif not ((s[0] == '[') or (s[0] == '(')):
      s = "[('" + s + "',)]";
    elif s[0] == '(':
      s = "[" + s + "]";
    else:
      pass;
    r = eval(s);
    return r;

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
          print "received data from ", raddr, " @", self.socksAddr[index], \
            " to ", self.addr[index], " len=", len(rdata);

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
            print "Unknown address", raddr


def signal_handler(signal_, frame):
  os.kill(os.getpid(), signal.SIGKILL);
  sys.exit(0)

if __name__ == "__main__":
  signal.signal(signal.SIGINT, signal_handler)
  p = Proxy();
  p.run();


