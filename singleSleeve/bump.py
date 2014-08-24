#!/usr/bin/python

import time;
import random;

import sys
sys.path.append('../lib')
from strip import *;


class Bump1(Effect):

  def __init__(self, strip2D):
    super(Bump1, self).__init__(strip2D);
    self.strip2D.strip.clear();

  def run(self, runtime = sys.maxint):
      
    self.strip2D.strip.clear([255, 255, 255]);

    for x in range(self.strip2D.lenx):
      self.strip2D.set(x, 0, [255, 0, 0]);
      self.strip2D.set(x, 1, [255, 0, 0]);
      self.strip2D.set(x, 2, [255, 0, 0]);
    for y in range(self.strip2D.leny):
      self.strip2D.set(0, y, [255, 0, 0]);
    self.strip2D.send();

    now = time.time();
    while (not self.quit) and ((time.time() - now) < runtime):
      
      for i in range(18):
        time.sleep(0.1);
        self.strip2D.rotu();
        self.strip2D.rotr();
        self.strip2D.send();
      for i in range(18):
        time.sleep(0.1);
        self.strip2D.rotd();
        self.strip2D.rotl();
        self.strip2D.send();

    self.quit = False;


if __name__ == "__main__":
  e = Bump1(Strip2D(7, 21));
  e.run();


