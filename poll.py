#!/usr/bin/python

"""
# default values -> broadcast at 192.168.89.255
./poll.py
# broadcast at 192.168.1.255
./poll.py addr=192.168.1.255
# send to multiple addresses (first with default port 6454).
./poll.py 'addr=[("192.168.1.255",),("localhost",7000)]'
"""

import time;
import sys;
from strip import Artnet;

def poll():
  artnet = Artnet();
  while True:
    artnet.poll();
    time.sleep(1.0);

poll();


