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
from night import *;
from matrix import *;
from power import *;
from weird1 import *;
from weird2 import *;
from weird3 import *;


lenx = 7;
leny = 21;

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
  [Night(strip2D), 30],
  [Fade1(strip2D), 3],
  [Fade2(strip2D), 3],
  [Stars1(strip2D), 15],
  [Stars2(strip2D), 10],
  [Hourglass(strip2D), 30],
  [Matrix(strip2D), 20],
  [Power(strip2D), 12],
  [Weird1(strip2D), 12],
  [Weird2(strip2D), 12],
  [Weird3(strip2D), 20],
];


def globalStop(self):
  print "globalStop"
  self.artnet.clear();
  self.send();

strip2D.strip.globalStop = globalStop

#count = 0;
count = random.randint(0, len(effects) - 1);    
dowait = False;


def manage():
  global count
  global dowait;
  while True:
    time.sleep(effects[count][1]);
    dowait = True;
    cnt = count;
    #count = (count + 1) % len(effects);
    count = random.randint(0, len(effects) - 1);    
    effects[cnt][0].quit = True;
    while dowait == True:
      time.sleep(0.1);
    dowait = True;


thread = threading.Thread(target = manage, args = []);
thread.daemon = True;
thread.start();

addr = getAddr();
strip2D.strip.artnet.addr = addr;

while True:
  #effects[count][0].run(effects[count][1] * 10);
  effects[count][0].run(random.randint(6, 30) * 10);
  for i in range(10):
    strip2D.strip.fade(.6);
    strip2D.send();
    time.sleep(0.05);
  strip2D.strip.artnet.clear();
  dowait = False;
  while dowait == False:
    time.sleep(0.1);


