#!/usr/bin/python

import time

import sys
sys.path.append('../lib')
from strip import *;


class Police1(Effect):

  color = [
    [0, 0, 255],
    [60, 60, 255],
    [140, 140, 255],
    [255, 255, 255],
    [140, 140, 255],
    [60, 60, 255],
    [0, 0, 255]];

  def __init__(self, strip2D):
    super(Police1, self).__init__(strip2D);
    self.strip2D.strip.clear();

  def run(self, runtime = sys.maxint):
    count = 0;
    count2 = 0;
    for x in range(self.strip2D.lenx):
      for y in range(self.strip2D.leny):
        self.strip2D.set(x, y, self.color[x]);
    now = time.time();
    while (not self.quit) and ((time.time() - now) < runtime):
      self.strip2D.rotr();
      self.strip2D.send();
      time.sleep(0.10);

    self.quit = False;


class Police2(Effect):
  color = [
    [0, 0, 255],
    [60, 60, 255],
    [140, 140, 255],
    [255, 255, 255],
    [140, 140, 255],
    [60, 60, 255],
    [0, 0, 255]];

  def __init__(self, strip2D):
    super(Police2, self).__init__(strip2D);
    self.strip2D.strip.clear();

  def rotr(self, y1, y2):
    for y in range(y1, y2):
      c = self.strip2D.get(self.strip2D.lenx - 1, y);
      for x in reversed(range(self.strip2D.lenx - 1)):
        self.strip2D.set(x + 1, y, self.strip2D.get(x, y));
      self.strip2D.set(0, y, c);

  def rotl(self, y1, y2):
    for y in range(y1, y2):
      c = self.strip2D.get(0, y);
      for x in range(self.strip2D.lenx - 1):
        self.strip2D.set(x, y, self.strip2D.get(x + 1, y));
      self.strip2D.set(self.strip2D.lenx - 1, y, c);

  def run(self, runtime = sys.maxint):
    for x in range(self.strip2D.lenx):
      for y in range(self.strip2D.leny):
        self.strip2D.set(x, y, self.color[x]);
    now = time.time();
    while (not self.quit) and ((time.time() - now) < runtime):
      self.rotr(0, 7);
      self.rotl(7, 14);
      self.rotr(14, 21);
      self.strip2D.send();
      time.sleep(0.10);

    self.quit = False;


class Police3(Effect):

  def __init__(self, strip2D):
    super(Police3, self).__init__(strip2D);
    self.strip2D.strip.clear();

  def color(self, count):
    if (count < 256):
      count -= 0;
      count /= 2;
      return [count, count, 255];
    if (count < 384):
      count = count - 256;
      return [128 + count, 128 + count, 255];
    if (count < 512):
      count = count - 384;
      return [255 - count, 255 - count, 255];
    if (count < 768):
      count = count - 512;
      count /= 2;
      return [128 - count, 128 - count, 255];

  def run(self, runtime = sys.maxint):
    count = 0;
    count2 = 0;
    now = time.time();
    while (not self.quit) and ((time.time() - now) < runtime):
      for i in range(self.strip2D.lenx):
        c = self.color(count2);
        self.strip2D.strip.clear(c);
        self.strip2D.send();
        time.sleep(0.03);
        count2 += 30;
        count2 = count2 % 768;

    self.quit = False;


"""
./police.py [1|2|3] addr=192.168.1.255
./police.py [1|2|3] 'addr=[("192.168.1.255", ), ("localhost", 7000)]'
./police.py [1|2|3] 'addr=[("192.168.1.255", 6454), ("localhost", 7000)]'
"""

if __name__ == "__main__":
  if (len(sys.argv) >= 2 and sys.argv[1] == "2"):
    e = Police2(Strip2D(7, 21));
  elif (len(sys.argv) >= 2 and sys.argv[1] == "3"):
    e = Police3(Strip2D(7, 21));
  else:
    e = Police1(Strip2D(7, 21));
  e.run();


