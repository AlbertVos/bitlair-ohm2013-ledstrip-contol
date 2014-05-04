#!/usr/bin/python

from strip import *;


class Power(Effect):

  def __init__(self, strip2D):
    super(Power, self).__init__(strip2D);

  def stepEffect(self, count):
    #if (count % 5) != 0:
    #  return;
    v = int(74.0 + 70.0 * math.sin(count / 20.0));
    self.strip2D.strip.clear();
    for i in range(v):
      self.strip2D.strip.set(i, self.getColor(i));

  def getColor(self, i):
    x = 255 * i / 144;
    if x < 0: x = 0;
    if x > 255: x = 255;
    return [x, 255 - x, 0];

if __name__ == "__main__":
  e = Power(Strip2D(7, 21));
  e.run();


