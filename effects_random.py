#!/usr/bin/python

import time;
import threading;
import random;
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
from flash import *;


lenx = 7;
leny = 21;

strip2D = Strip2D(lenx, leny);
effects = [
  [Police1(strip2D)],
  [Rainbow(strip2D)],
  [Police2(strip2D)],
  [Bump1(strip2D)],
  [Police3(strip2D)],
  [CMorph(strip2D)],
  [Plasma(strip2D)],
  [Fire(strip2D)],
  [Night(strip2D)],
  [Fade2(strip2D)],
  [Fade1(strip2D)],
  [Hourglass(strip2D)],
  [Matrix(strip2D)],
  [Power(strip2D)],
  [Weird1(strip2D)],
  [Weird2(strip2D)],
  [Flash(strip2D)],
];


def globalStop(self):
  print "globalStop"
  self.artnet.clear();
  self.send();

strip2D.strip.globalStop = globalStop

count = 0;
dowait = False;
rnd_time = 0;


def manage():
  global count
  global dowait;
  while True:
    time.sleep(rnd_time);
    dowait = True;
    cnt = count;
    while cnt == count:
      count = random.randint(1, len(effects)) % len(effects);    
    effects[cnt][0].quit = True;
    while dowait == True:
      time.sleep(0.1);
    dowait = True;


random.seed();

thread = threading.Thread(target = manage, args = []);
thread.daemon = True;
thread.start();

addr = getAddr();
strip2D.strip.artnet.addr = addr;

while True:
  rnd_time = random.randint(30, 90);  
  effects[count][0].run(rnd_time * 10);
  print effects[count],'for',rnd_time,'seconds.';
  for i in range(10):
    strip2D.strip.fade(.6);
    strip2D.send();
    time.sleep(0.05);
  strip2D.strip.artnet.clear();
  dowait = False;
  while dowait == False:
    time.sleep(0.1);


