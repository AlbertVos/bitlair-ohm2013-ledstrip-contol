#!/usr/bin/python

import time;
import threading;

from strip import *;

from police import *;
from rainbow import *;
from bump import *;
from cmorph import *;
from lemmings import *;
from plasma import *;


lenx = 7;
leny = 21;

addr = [
  [("192.168.89.133", 6454), ("localhost", 7000)],
  [("192.168.89.131", 6454), ("localhost", 7001)],
  [("192.168.89.135", 6454), ("localhost", 7002)],
  [("192.168.89.132", 6454), ("localhost", 7003)],
  [("192.168.89.134", 6454), ("localhost", 7004)],
  [("192.168.89.149", 6454), ("localhost", 7005)],
];

colors = [
  [255, 0, 0],
  [255, 96, 0],
  [255, 255, 0],
  [0, 255, 0],
  [0, 255, 255],
  [0, 0, 255],
  [255, 0, 255],
];


#strip2D = Strip2D(lenx, leny);
#police = Police3(strip2D);
#police.run();

strips = [];

def fillThird(strip, index, color):
  for y in range(7):
    for x in range(7):
      strip.set(x, y + index * 7, color);

for i in range(len(addr)):
  s = Strip2D(lenx, leny);
  s.strip.artnet.addr = addr[i];
  strips.append(s);

colorCount = 0;
while True:
  n = 2 * len(addr) + 2;
  for i in range(len(addr)):
    s = strips[i];
    if i == 0:
      c = colors[(colorCount + 0) % len(colors)];
      fillThird(s, 0, c);
      c = colors[(colorCount + 1) % len(colors)];
      fillThird(s, 1, c);
      c = colors[(colorCount + 2) % len(colors)];
      fillThird(s, 2, c);
    elif i == len(addr) - 1:
      c = colors[(colorCount + i + 2) % len(colors)];
      fillThird(s, 2, c);
      c = colors[(colorCount + i + 3) % len(colors)];
      fillThird(s, 1, c);
      c = colors[(colorCount + i + 4) % len(colors)];
      fillThird(s, 0, c);
    else:
      c = colors[(colorCount + i + 2) % len(colors)];
      fillThird(s, 2, c);
      fillThird(s, 1, [0, 0, 0]);
      c = colors[(colorCount + n - i) % len(colors)];
      fillThird(s, 0, c);
    s.send();
  colorCount += 1;
  time.sleep(0.1);

ipcnt = 0;
while True:
  strip2D.strip.artnet.addr = addr[ipcnt];
  ipcnt = (ipcnt + 1) % len(addr);
  effects[count].run(20);
  strip2D.strip.artnet.clear();
  dowait = False;
  while dowait == False:
    time.sleep(0.15);

while False:
  strip2D.strip.artnet.host = ip[ipcnt];
  ipcnt = (ipcnt + 1) % len(ip);
  effects[count].run();
  strip2D.strip.artnet.clear();
  dowait = False;
  while dowait == False:
    time.sleep(0.1);

strip2D.strip.stop();
os.kill(os.getpid(), signal.SIGKILL);

#thread = threading.Thread(target = discover, args = []);
#thread.daemon = True;
#thread.start();
#thread.join();


