#!/usr/bin/python

import time

import sys
sys.path.append('../lib')
from strip import *;

# Orange flasher

class Flash(Effect):

  def __init__(self, strip2D):
    super(Flash, self).__init__(strip2D);
    self.strip2D.strip.clear([255, 255, 255]);

  def step(self, count):
    self.strip2D.set(0, 0, [255, 0, 0]);
    self.strip2D.set(1, 1, [0, 255, 0]);
    self.strip2D.set(2, 2, [0, 0, 255]);
    self.strip2D.set(3, 3, [0, 255, 255]);
    self.strip2D.send();
    time.sleep(1.0);


if __name__ == "__main__":
  e = Flash(Strip2D(7, 21));
  e.run();


