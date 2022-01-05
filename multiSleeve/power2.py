#!/usr/bin/env python3

import time
import threading
import sys
import math
sys.path.append('../lib')
sys.path.append('../singleSleeve')
from strip import Strip2D, getAddr
from power import Power


lenx = 7
leny = 21
strips = []
count = 0

addr = getAddr()

for i, address in enumerate(addr):
  s = Strip2D(lenx, leny)
  s.strip.artnet.addr = [address]
  p = Power(s, i * .3)
  strips.append(p)

if False: # pylint: disable=using-constant-test
  for i, s in enumerate(strips):
    s.auto = True
    thread = threading.Thread(target = s.run, args=[])
    thread.daemon = True
    thread.start()
  while True:
    time.sleep(2)

if True: # pylint: disable=using-constant-test
  for i, s in enumerate(strips):
    s.auto = False
    s.offset = 13 * i
    thread = threading.Thread(target = s.run, args=[])
    thread.daemon = True
    thread.start()
  while True:
    for i, s in enumerate(strips):
      s.v = int(74.0 + 70.0 * math.sin((count + 15 * i) / 20.0))
    time.sleep(.02)
    count += 1
