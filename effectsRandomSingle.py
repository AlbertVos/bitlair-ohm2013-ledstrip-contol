#!/usr/bin/env python3

import time
import threading
import random

import sys
sys.path.append('lib')
from strip import Strip2D, getAddr

sys.path.append('singleSleeve')
from bump import Bump1
from cmorph import CMorph
from fade import Fade1, Fade2
from fire import Fire
from fire2 import Fire2
from hourglass import Hourglass
from lemmings import Lemmings1
from plasma import Plasma
from police import Police1, Police2, Police3
from rainbow import Rainbow
from stars import Stars1, Stars2
from night import Night
from matrix import Matrix
from power import Power
from weird1 import Weird1
from weird2 import Weird2
from weird3 import Weird3
from flash import Flash
from lighthouse import Lighthouse


lenx = 7
leny = 21

strip2D = Strip2D(lenx, leny)
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
  [Fire2(strip2D), 30],
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
  [Lighthouse(strip2D), 10],
  [Flash(strip2D), 10],
]


def globalStop(self):
  print( "globalStop" )
  self.artnet.clear()
  self.send()

strip2D.strip.globalStop = globalStop

#count = 0
count = random.randint(0, len(effects) - 1)
dowait = False


def manage():
  global count
  global dowait
  while True:
    time.sleep(effects[count][1])
    dowait = True
    cnt = count
    # Run fixed sequence of effects
    #count = (count + 1) % len(effects)
    # Run random sequence of effects
    count = random.randint(0, len(effects) - 1)
    effects[cnt][0].quit = True
    while not dowait:
      time.sleep(0.1)
    dowait = True


thread = threading.Thread(target = manage, args = [])
thread.daemon = True
thread.start()

addr = getAddr()
strip2D.strip.artnet.addr = addr

while True:
  # Print effect name
  #print( "---", type(effects[count][0]).__name__, "---" )

  #effects[count][0].run(effects[count][1] * 10)
  effects[count][0].run(random.randint(6, 30) * 10)
  for i in range(10):
    strip2D.strip.fade(.6)
    strip2D.send()
    time.sleep(0.05)
  #strip2D.strip.artnet.clear()
  dowait = False
  while not dowait:
    time.sleep(0.1)
