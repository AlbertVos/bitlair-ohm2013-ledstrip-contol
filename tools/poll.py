#!/usr/bin/env python3

"""
# default values -> broadcast at 192.168.89.255
./poll.py
# broadcast at 192.168.1.255
./poll.py addr=192.168.1.255
# send to multiple addresses (first with default port 6454).
./poll.py 'addr=[("192.168.1.255",),("localhost",7000)]'
"""

import time;
import signal;
import sys;
sys.path.append('../lib')
import os;
from strip import Artnet;

def poll():
  global artnet;
  artnet = Artnet();
  artnet.addr = [("255.255.255.255", 6454)];
  while True:
    artnet.poll();
    time.sleep(1.0);

def signal_handler(signal_, frame):
  artnet.close();
  os.kill(os.getpid(), signal.SIGKILL);
  sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
poll();


