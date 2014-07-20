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

colors = [
  [0, 255, 255],
  [255, 215, 0],
];

pixels = [
  #0              5              10             15             20
  [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] , 
  [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0] , 
  [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
];

pixels = [
  #0              5              10             15             20
  [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0] , 
  [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0] , 
  [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0] , 
  [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0] , 
  [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0]
];


strips = [];

def fillFifth(strip, index, color):
  for y in range(21 / 5):
    for x in range(7):
      strip.set(x, y + index * 21 / 5, color);

def rainbow(count):
  count %= 1536;
  if count < 256:
    count -= 0;
    return [255, count, 0];
  if count < 512:
    count -= 256;
    return [255 - count, 255, 0];
  if count < 768:
    count -= 512;
    return [0, 255, count];
  if count < 1024:
    count -= 768;
    return [0, 255 - count, 255];
  if count < 1280:
    count -= 1024;
    return [count, 0, 255];
  if count < 1536:
    count -= 1280;
    return [255, 0, 255 - count];
  return [0, 0, 0];

def getColor(count, inv):
  c = rainbow(count);
  if inv > 0:
    return c;
  else:
    return [255 - c[0], 255 - c[1], 255 - c[2]];


addr = getAddr();

for i in range(len(addr)):
  s = Strip2D(lenx, leny);
  s.strip.artnet.addr = [addr[i]];
  strips.append(s);

count = 0;
while True:
  xx = count % (len(pixels[0]) - len(strips));
  count += 1;

  for x in range(len(strips)):
    for y in range(len(pixels)):
      s = strips[len(strips) - 1 - x];
      fillFifth(s, y, getColor(count, pixels[y][xx + x]));
    s.fade(.25);
    s.send();
  time.sleep(0.2);


