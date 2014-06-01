#!/usr/bin/python

import time;
import threading;

from strip import *;

from power import *;


lenx = 7;
leny = 21;

addr = [
  [("192.168.93.141", 6454)],
  [("192.168.93.138", 6454)],
  [("192.168.93.139", 6454)],
  [("192.168.93.147", 6454)],
  [("192.168.93.142", 6454)],
  [("192.168.93.140", 6454)],
  [("192.168.93.145", 6454)],
  [("192.168.93.137", 6454)],
];


strips = [];
count = 0;

for i in range(len(addr)):
  s = Strip2D(lenx, leny);
  s.strip.artnet.addr = addr[i];
  p = Power(s, i * .3);
  strips.append(p);

if False:
  for i in range(len(strips)):
    s = strips[i];
    s.auto = True;
    thread = threading.Thread(target = s.run, args=[s]);
    thread.daemon = True;
    thread.start();
  while True:
    time.sleep(2);

if True:
  for i in range(len(strips)):
    s = strips[i];
    s.auto = False;
    s.offset = 13 * i;
    thread = threading.Thread(target = s.run, args=[s]);
    thread.daemon = True;
    thread.start();
  while True:
    for i in range(len(strips)):
      s = strips[i];
      s.v = int(74.0 + 70.0 * math.sin((count + 15 * i) / 20.0));
    time.sleep(.02);
    count += 1;


strip2D.strip.stop();
os.kill(os.getpid(), signal.SIGKILL);


