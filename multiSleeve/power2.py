#!/usr/bin/env python3

import time;
import threading;
import sys;
sys.path.append('../lib')
sys.path.append('../singleSleeve')
from strip import *;
from power import *;


lenx = 7;
leny = 21;
strips = [];
count = 0;

addr = getAddr();

for i in range(len(addr)):
  s = Strip2D(lenx, leny);
  s.strip.artnet.addr = [addr[i]];
  p = Power(s, i * .3);
  strips.append(p);

if False:
  for i in range(len(strips)):
    s = strips[i];
    s.auto = True;
    thread = threading.Thread(target = s.run, args=[]);
    thread.daemon = True;
    thread.start();
  while True:
    time.sleep(2);

if True:
  for i in range(len(strips)):
    s = strips[i];
    s.auto = False;
    s.offset = 13 * i;
    thread = threading.Thread(target = s.run, args=[]);
    thread.daemon = True;
    thread.start();
  while True:
    for i in range(len(strips)):
      s = strips[i];
      s.v = int(74.0 + 70.0 * math.sin((count + 15 * i) / 20.0));
    time.sleep(.02);
    count += 1;


