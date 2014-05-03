#!/usr/bin/python

import time;
import random;
from strip import *;


class Stars(Effect):

  def __init__(self, strip2D):
    super(Stars, self).__init__(strip2D);
    self.getColor = self.getColor1

  def stepEffect(self, count):
    if (count % 5) != 0:
      return;
    self.strip2D.strip.fade(.8);
    for i in range(1):
      self.strip2D.set(random.randint(0, 6), random.randint(0, 20) \
        , self.getColor());

  def getColor1(self):
    return [255, 255, 255];

  def getColor2(self):
    return [random.randint(0, 255), random.randint(0, 255) \
      , random.randint(0, 255)];


if __name__ == "__main__":
  e = Stars(Strip2D(7, 21));
  e.run();


