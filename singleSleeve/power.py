#!/usr/bin/python

import sys
sys.path.append('../lib')
from strip import *;


class Power(Effect):
  auto = True;
  v = 0;

  def __init__(self, strip2D, offset = 0.0):
    super(Power, self).__init__(strip2D);
    self.strip2D.strip.clear();
    self.offset = offset;

  def step(self, count):
    #if (count % 5) != 0:
    #  return;
    if self.auto:
      self.v = int(74.0 + 70.0 * math.sin((count + self.offset) / 20.0));
    self.strip2D.strip.clear();
    for i in range(self.v):
      self.strip2D.strip.set(i, self.getColor(i));

  def getColor(self, i):
    x = 255 * i / 144;
    if x < 0: x = 0;
    if x > 255: x = 255;
    return [x, 255 - x, 0];

if __name__ == "__main__":
  e = Power(Strip2D(7, 21));
  e.run();


