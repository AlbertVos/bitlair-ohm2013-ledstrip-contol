#!/usr/bin/python

import time

import sys
sys.path.append('../lib')
from strip import *;


class Fade1(Effect):

  def __init__(self, strip2D):
    super(Fade1, self).__init__(strip2D);
    self.strip2D.strip.clear();

  def run(self, runtime = sys.maxint):
      
    self.strip2D.strip.clear([255, 255, 255]);

    count = 0;
    count2 = 0;
    now = time.time();
    while (not self.quit) and ((time.time() - now) < runtime):
      for i in range(self.strip2D.lenx):
        self.strip2D.strip.fade(.6);
        self.strip2D.rotr();
        for y in range(self.strip2D.leny):
          self.strip2D.set(count, y, self.color(count2));
        self.strip2D.send();
        time.sleep(0.02);
        count2 += 1;
        count2 = count2 % 1536;
      count += 1;
      count = count % self.strip2D.lenx;

    self.quit = False;

  def color(self, count):
    if (count < 256):
      count -= 0;
      return [255, 0, 255 - count];
    if (count < 512):
      count -= 256;
      return [255, count, 0];
    if (count < 768):
      count -= 512;
      return [255 - count, 255, 0];
    if (count < 1024):
      count -= 768;
      return [0, 255, count];
    if (count < 1280):
      count -= 1024;
      return [0, 255 - count, 255];
    if (count < 1536):
      count -= 1280;
      return [count, 0, 255];


class Fade2(Effect):

  def __init__(self, strip2D):
    super(Fade2, self).__init__(strip2D);
    self.strip2D.strip.clear();

  def run(self, runtime = sys.maxint):
      
    self.strip2D.strip.clear([255, 255, 255]);

    count = 0;
    now = time.time();
    while (not self.quit) and ((time.time() - now) < runtime):
      for i in range(self.strip2D.lenx):
        self.strip2D.strip.fade(.6);
        self.strip2D.rotr();
        for y in range(self.strip2D.leny):
          self.strip2D.set(count, y, [255, 90, 0]);
        self.strip2D.send();
        time.sleep(0.02);
      count += 1;
      count = count % self.strip2D.lenx;

    self.quit = False;


"""
./fade.py [1|2] addr=192.168.1.255
./fade.py [1|2] 'addr=[("192.168.1.255", ), ("localhost", 7000)]'
./fade.py [1|2] 'addr=[("192.168.1.255", 6454), ("localhost", 7000)]'
"""

if __name__ == "__main__":
  if (len(sys.argv) >= 2 and sys.argv[1] == "2"):
    e = Fade2(Strip2D(7, 21));
  else:
    e = Fade1(Strip2D(7, 21));
  e.run();


