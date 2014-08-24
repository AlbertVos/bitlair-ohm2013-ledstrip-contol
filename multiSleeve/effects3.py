#!/usr/bin/python

import time;

import sys
sys.path.append('../lib')
from strip import *;


lenx = 7;
leny = 21;

colors = [
  [255, 0, 0],
  [255, 96, 0],
  [255, 255, 0],
  [0, 255, 0],
  [0, 255, 255],
  [0, 0, 255],
  [255, 0, 255],
];

strips = [];
addr = getAddr();

def signal_handler(signal_, frame):
  #print('Stopping, bye ...')
  stop();
  os.kill(os.getpid(), signal.SIGKILL);
  sys.exit(0)

def stop():
  for i in range(len(strips)):
    strips[i].strip.clear();
    strips[i].strip.send();
    strips[i].strip.stop();

#strip2D.strip.globalStop = globalStop

def fillThird(strip, index, color):
  for y in range(7):
    for x in range(7):
      strip.set(x, y + index * 7, color);

for i in range(len(addr)):
  s = Strip2D(lenx, leny);
  s.strip.artnet.addr = [addr[i]];
  strips.append(s);

# Set signal handler after strips are created to override handler.
signal.signal(signal.SIGINT, signal_handler)

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


