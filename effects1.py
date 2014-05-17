#!/usr/bin/python

import time;
import threading;
from strip import *;

from bump import *;
from cmorph import *;
from fade import *;
from fire import *;
from hourglass import *;
from lemmings import *;
from plasma import *;
from police import *;
from rainbow import *;
from stars import *;


lenx = 7;
leny = 21;

ip = [
  "192.168.89.150", 
  "192.168.89.133", 
  "192.168.89.131", 
  "192.168.89.135", 
  "192.168.89.132", 
  "192.168.89.134", 
  "192.168.89.149", 
];
ip = [
  "192.168.89.255", 
];

strip2D = Strip2D(lenx, leny);
effects = [
  [Police1(strip2D), 3],
  [Rainbow(strip2D), 10],
  [Police2(strip2D),  3],
  [Bump1(strip2D), 3],
  [Police3(strip2D), 3],
  [Lemmings1(strip2D), 10],
  [CMorph(strip2D), 7],
  [Plasma(strip2D), 30],
  [Fire(strip2D), 30],
  [Fade1(strip2D), 3],
  [Fade2(strip2D), 3],
  [Stars1(strip2D), 15],
  [Stars2(strip2D), 10],
  [Hourglass(strip2D), 30],
];


def globalStop(self):
  print "globalStop"
  for i in range(len(ip)):
    addr[0] = (ip[i], addr[0][1]);
    addr[1] = (addr[1][0], 7000 + i);
    self.artnet.addr = addr;
    self.artnet.clear();
    self.send();

strip2D.strip.globalStop = globalStop

count = 0;
ipcnt = 0;
dowait = False;

if False:
  while True:
    strip2D.strip.artnet.host = ip[ipcnt];
    ipcnt = (ipcnt + 1) % len(ip);
    effects[count][0].run(effects[count][1]);
    strip2D.strip.artnet.clear();
    count = (count + 1) % len(effects);



def manage():
  global count
  global dowait;
  while True:
    time.sleep(effects[count][1]);
    dowait = True;
    cnt = count;
    count = (count + 1) % len(effects);
    effects[cnt][0].quit = True;
    while dowait == True:
      time.sleep(0.1);
    dowait = True;


thread = threading.Thread(target = manage, args = []);
thread.daemon = True;
thread.start();

addr = [("192.168.89.255", 6454), ("localhost", 7000)]

while True:
  addr[0] = (ip[ipcnt], addr[0][1]);
  addr[1] = (addr[1][0], 7000 + ipcnt);
  ipcnt = (ipcnt + 1) % len(ip);
  strip2D.strip.artnet.addr = addr;
  effects[count][0].run(effects[count][1] * 10);
  for i in range(10):
    strip2D.strip.fade(.6);
    strip2D.send();
    time.sleep(0.05);
  strip2D.strip.artnet.clear();
  dowait = False;
  while dowait == False:
    time.sleep(0.1);

while False:
  strip2D.strip.artnet.addr = [(ip[ipcnt], 6454)];
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

