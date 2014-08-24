#!/usr/bin/python

import time
import sys

import sys
sys.path.append('../lib')
from strip import *;

# From: http://www.mobile1up.com/lemmings/blog/index-old.php
#   http://www.mobile1up.com/lemmings/blog/pictures/lemmings-walker-sprites.png
# 
# http://crisp.tweakblogs.net/blog/3881/dhtml-lemmings-primer.html
# http://tweakers.net/redactieblogs/70169/html-5-de-toekomst-van-gaming-op-het-web.html

class Lemmings1(Effect):
  step = [1, 0, 0, 0, 1, 0, 0, 0]

  sprites = [
  [[0, 0, 0, 0, 0, 0],
  [0, 1, 1, 1, 1, 0],
  [0, 1, 1, 3, 0, 0],
  [0, 0, 3, 3, 3, 0],
  [0, 0, 3, 2, 0, 0],
  [0, 0, 3, 2, 0, 0],
  [0, 0, 3, 2, 0, 0],
  [0, 0, 2, 2, 0, 0],
  [0, 3, 2, 2, 0, 0],
  [0, 0, 3, 3, 0, 0]],

  [[0, 0, 1, 0, 1, 0],
  [0, 1, 1, 1, 0, 0],
  [0, 1, 1, 3, 0, 0],
  [0, 0, 3, 3, 3, 0],
  [0, 0, 3, 2, 0, 0],
  [0, 3, 2, 2, 0, 0],
  [0, 3, 2, 2, 0, 3],
  [0, 0, 2, 2, 0, 3],
  [0, 2, 2, 0, 3, 0],
  [0, 3, 3, 0, 0, 0]],

  [[0, 0, 0, 0, 0, 0],
  [0, 1, 0, 1, 0, 0],
  [0, 1, 1, 1, 0, 0],
  [0, 0, 1, 3, 0, 0],
  [0, 0, 3, 3, 3, 0],
  [0, 3, 3, 2, 0, 0],
  [0, 3, 2, 2, 0, 0],
  [3, 3, 2, 2, 2, 0],
  [0, 2, 2, 2, 2, 0],
  [3, 3, 0, 0, 3, 3]],

  [[0, 0, 0, 0, 0, 0],
  [0, 1, 1, 1, 0, 0],
  [0, 1, 1, 3, 1, 0],
  [0, 0, 3, 3, 3, 0],
  [0, 0, 3, 2, 0, 0],
  [0, 0, 3, 2, 0, 0],
  [0, 3, 2, 2, 0, 0],
  [0, 0, 2, 2, 0, 0],
  [3, 2, 2, 2, 2, 0],
  [3, 0, 0, 3, 3, 0]],

  [[0, 0, 0, 0, 0, 0],
  [0, 1, 1, 1, 1, 0],
  [0, 1, 1, 3, 0, 0],
  [0, 1, 3, 3, 3, 0],
  [0, 0, 3, 2, 0, 0],
  [0, 0, 2, 3, 0, 0],
  [0, 0, 3, 2, 0, 0],
  [0, 0, 2, 2, 0, 0],
  [0, 3, 2, 2, 0, 0],
  [0, 0, 3, 3, 0, 0]],

  [[0, 0, 1, 0, 1, 0],
  [0, 1, 1, 1, 0, 0],
  [0, 1, 1, 3, 0, 0],
  [0, 0, 3, 3, 3, 0],
  [0, 0, 3, 2, 0, 0],
  [0, 0, 2, 3, 0, 0],
  [0, 0, 2, 3, 0, 3],
  [0, 0, 2, 2, 0, 3],
  [0, 2, 2, 0, 3, 0],
  [0, 3, 3, 0, 0, 0]],

  [[0, 0, 0, 0, 0, 0],
  [0, 1, 0, 1, 0, 0],
  [0, 1, 1, 1, 0, 0],
  [0, 0, 1, 3, 0, 0],
  [0, 0, 3, 3, 3, 0],
  [0, 0, 2, 3, 0, 0],
  [0, 0, 2, 3, 0, 0],
  [0, 0, 2, 2, 3, 0],
  [0, 2, 2, 2, 2, 0],
  [3, 3, 0, 0, 3, 3]],

  [[0, 0, 0, 0, 0, 0],
  [0, 0, 1, 1, 0, 0],
  [0, 1, 1, 3, 1, 0],
  [0, 1, 3, 3, 3, 0],
  [0, 0, 3, 2, 0, 0],
  [0, 0, 3, 2, 0, 0],
  [0, 0, 2, 3, 0, 0],
  [0, 0, 2, 2, 0, 0],
  [3, 2, 2, 2, 2, 0],
  [3, 0, 0, 3, 3, 0]]];

  palette1 = [[0, 181, 0], [90, 99, 255], [255, 239, 222]];
  palette2 = [[0, 90, 0], [45, 45, 127], [127, 120, 111]];
  palette3 = [[0, 45, 0], [10, 10, 64], [64, 60, 55]];
  palette = palette3;

  def __init__(self, strip2D):
    super(Lemmings1, self).__init__(strip2D);
    self.strip2D.strip.clear();

  def run(self, runtime = sys.maxint):
    start = 10;
    end = 77;
    count = start - self.strip2D.lenx;

    now = time.time();
    self.strip2D.strip.artnet.clear();
    while (not self.quit) and ((time.time() - now) < runtime):
      for i in range(len(self.sprites)):
        self.strip2D.strip.clear();
        sprite = self.sprites[i];
        h = len(sprite);
        for y in range(h):
          line = sprite[y];
          w = len(line);
          for x in range(w):
            c = line[x];
            xx = x + count;
            if (c > 0) and (xx >= start) and (xx < end):
              yy = h - 1 - y; 
              self.strip2D.strip.set( \
                xx + yy * self.strip2D.lenx, self.palette[c - 1]);
        if True:
          count += self.step[i];
          if count > 70:
            count = start - self.strip2D.lenx;
        else:
          count = 30;

        self.strip2D.send();
        time.sleep(0.15);

    self.quit = False;


"""
./lemmings.py 'addr=[("localhost", 7000)]'
"""

if __name__ == "__main__":
  e = Lemmings1(Strip2D(7, 21));
  e.run();


