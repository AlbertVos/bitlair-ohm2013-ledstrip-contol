#!/usr/bin/python

import time;
import random;

import sys
sys.path.append('../lib')
from strip import *;


class Lighthouse(Effect):

  def __init__(self, strip2D):
    super(Lighthouse, self).__init__(strip2D);
    self.strip2D.strip.clear();

  def run(self, runtime = sys.maxint):
      
    self.strip2D.strip.clear();

    x = 5;
    for y in range(self.strip2D.leny):
      if y % 7 == 0:
        x -= 1;
      self.strip2D.set(x - 1, y, [40, 40, 40]);
      self.strip2D.set(x, y, [255, 255, 255]);
    self.strip2D.send();

    now = time.time();
    while (not self.quit) and ((time.time() - now) < runtime):
      time.sleep(0.2);
      self.strip2D.rotr();
      self.strip2D.send();

    self.quit = False;


if __name__ == "__main__":
  e = Lighthouse(Strip2D(7, 21));
  e.run();


