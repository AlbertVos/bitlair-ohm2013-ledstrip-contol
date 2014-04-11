#!/usr/bin/python

import time;
import threading;
from strip import *;

from police import *;
from rainbow import *;
from bump import *;
from cmorph import *;
from lemmings import *;


lenx = 7;
leny = 21;

ip = [
  "192.168.89.133", 
  "192.168.89.131", 
  "192.168.89.135", 
  "192.168.89.132", 
  "192.168.89.134", 
];
addr = [("192.168.89.255", 6454), ("localhost", 7000)]

#strip2D = Strip2D(lenx, leny);
#police = Police3(strip2D);
#police.run();

strip2D = Strip2D(lenx, leny);
effects = [
  Police1(strip2D), 
  Rainbow(strip2D),
  Police2(strip2D), 
  Bump1(strip2D),
  Police3(strip2D),
  Lemmings1(strip2D),
  CMorph(strip2D),
];

count = 0;
ipcnt = 0;
dowait = False;

def manage():
  global count
  global dowait;
  while True:
    time.sleep(4);
    dowait = True;
    cnt = count;
    count = (count + 1) % len(effects);
    effects[cnt].quit = True;
    while dowait == True:
      time.sleep(0.1);
    dowait = True;


thread = threading.Thread(target = manage, args = []);
thread.daemon = True;
thread.start();

while True:
  addr[0] = (ip[ipcnt], addr[0][1]);
  addr[1] = (addr[1][0], 7000 + ipcnt);
  ipcnt = (ipcnt + 1) % len(ip);
  strip2D.strip.artnet.addr = addr;
  effects[count].run(20);
  strip2D.strip.artnet.clear();
  dowait = False;
  while dowait == False:
    time.sleep(0.1);

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


