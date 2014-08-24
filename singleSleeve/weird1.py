#!/usr/bin/python

import time;
import random;

import sys
sys.path.append('../lib')
from strip import *;


class Weird1(Effect):
  bg1 = [0, 50, 0];
  bg2 = [50, 50, 50];
  fg = [180, 0, 0];
  bgSpeed = 4;
  bgSpeedCount = 0;
  fgSpeed = 2;
  fgSpeedCount = 0;
  fgCount = 0;

  def __init__(self, strip2D):
    super(Weird1, self).__init__(strip2D);
    self.strip2D.strip.clear();
    self.strip2D.send();

  def step(self, count):
    if self.bgSpeedCount <= 0:
      (self.bg1, self.bg2) = (self.bg2, self.bg1);
      self.bgSpeedCount = self.bgSpeed;
    else:
      self.bgSpeedCount -= 1;
    if self.fgSpeedCount <= 0:
      self.fgCount += 1;
      if self.fgCount > 10:
        self.fgCount = 0;
      self.fgSpeedCount = self.fgSpeed;
    else:
      self.fgSpeedCount -= 1;

    for y in range(21):
      for x in range(7):
        if y % 2 == 0:
          self.strip2D.set(x, y, self.bg1);
        else:
          self.strip2D.set(x, y, self.bg2);
      
    for x in range(7):
      self.strip2D.set(x, 10 + self.fgCount, self.fg);
      self.strip2D.set(x, 10 - self.fgCount, self.fg);
        

if __name__ == "__main__":
  e = Weird1(Strip2D(7, 21));
  e.run();


